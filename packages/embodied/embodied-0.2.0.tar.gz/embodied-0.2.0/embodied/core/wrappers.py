import functools

import numpy as np

from . import base


class TimeLimit(base.Wrapper):

  def __init__(self, env, duration):
    super().__init__(env)
    self._duration = duration
    self._step = 0
    self._done = False

  def step(self, action):
    if action['reset'] or self._done:
      self._step = 0
      self._done = False
      action.update(reset=True)
      return self.env.step(action)
    self._step += 1
    obs = self.env.step(action)
    if self._duration and self._step >= self._duration:
      obs['is_last'] = True
    self._done = obs['is_last']
    return obs


class ActionRepeat(base.Wrapper):

  def __init__(self, env, repeat):
    super().__init__(env)
    self._repeat = repeat
    self._done = False

  def step(self, action):
    if action['reset'] or self._done:
      return self.env.step(action)
    reward = 0.0
    for _ in range(self._repeat):
      obs = self.env.step(action)
      reward += obs['reward']
      if obs['is_last'] or obs['is_terminal']:
        break
    obs['reward'] = reward
    self._done = obs['is_last']
    return obs


class NormalizeAction(base.Wrapper):

  def __init__(self, env, key='action'):
    super().__init__(env)
    self._key = key
    space = env.act_space[key]
    self._mask = np.isfinite(space.low) & np.isfinite(space.high)
    self._low = np.where(self._mask, space.low, -1)
    self._high = np.where(self._mask, space.high, 1)

  @property
  def act_space(self):
    low = np.where(self._mask, -np.ones_like(self._low), self._low)
    high = np.where(self._mask, np.ones_like(self._low), self._high)
    space = base.Space(np.float32, None, low, high)
    return {**self.env.act_space, self._key: space}

  def step(self, action):
    orig = (action[self._key] + 1) / 2 * (self._high - self._low) + self._low
    orig = np.where(self._mask, orig, action[self._key])
    return self.env.step({**action, self._key: orig})


class OneHotAction(base.Wrapper):

  def __init__(self, env, key='action'):
    super().__init__(env)
    self._count = int(env.act_space[key].high)
    self._key = key

  @property
  def act_space(self):
    shape = (self._count,)
    space = base.Space(np.float32, shape, 0, 1)
    space.sample = functools.partial(self._sample_action, self._count)
    space.discrete = True
    return {**self.env.act_space, self._key: space}

  def step(self, action):
    index = np.argmax(action[self._key]).astype(int)
    reference = np.zeros_like(action[self._key])
    reference[index] = 1
    if not action['reset']:
      if not np.allclose(reference, action[self._key]):
        raise ValueError(f'Invalid one-hot action:\n{action}')
    return self.env.step({**action, self._key: index})

  @staticmethod
  def _sample_action(count):
    index = np.random.randint(0, count)
    reference = np.zeros(count, dtype=np.float32)
    reference[index] = 1.0
    return reference


class ResizeImage(base.Wrapper):

  def __init__(self, env, size=(64, 64)):
    super().__init__(env)
    self._size = size
    self._keys = [
        k for k, v in env.obs_space.items()
        if len(v.shape) > 1 and v.shape[:2] != size]
    print(f'Resizing keys {",".join(self._keys)} to {self._size}.')
    if self._keys:
      from PIL import Image
      self._Image = Image

  @property
  def obs_space(self):
    spaces = self.env.obs_space
    for key in self._keys:
      shape = self._size + spaces[key].shape[2:]
      spaces[key] = base.Space(np.uint8, shape)
    return spaces

  def step(self, action):
    obs = self.env.step(action)
    for key in self._keys:
      obs[key] = self._resize(obs[key])
    return obs

  def _resize(self, image):
    image = self._Image.fromarray(image)
    image = image.resize(self._size, self._Image.NEAREST)
    image = np.array(image)
    return image


class RenderImage(base.Wrapper):

  def __init__(self, env, key='image'):
    super().__init__(env)
    self._key = key
    self._shape = self.env.render().shape

  @property
  def obs_space(self):
    spaces = self.env.obs_space
    spaces[self._key] = base.Space(np.uint8, self._shape)
    return spaces

  def step(self, action):
    obs = self.env.step(action)
    obs[self._key] = self.env.render()
    return obs
