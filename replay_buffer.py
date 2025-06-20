# This code is shamelessly stolen from
# https://github.com/openai/baselines/blob/master/baselines/deepq/replay_buffer.py
import numpy as np
import random


class ReplayBuffer(object):
    def __init__(self, size):
        """Create Replay buffer.
        Parameters
        ----------
        size: int
            Max number of transitions to store in the buffer. When the buffer
            overflows the old memories are dropped.
        """
        self._storage = []
        self._maxsize = size
        self._next_idx = 0

    def __len__(self):
        return len(self._storage)

    def add(self, obs_t, action, reward, obs_tp1, done):
        data = (obs_t, action, reward, obs_tp1, done)

        if self._next_idx >= len(self._storage):
            self._storage.append(data)
        else:
            self._storage[self._next_idx] = data
        self._next_idx = (self._next_idx + 1) % self._maxsize

    def _encode_sample(self, idxes):
        obses_t, actions, rewards, obses_tp1, dones = [], [], [], [], []
        for i in idxes:
            data = self._storage[i]
            obs_t, action, reward, obs_tp1, done = data
            obses_t.append(np.asarray(obs_t))
            actions.append(np.asarray(action))
            rewards.append(reward)
            obses_tp1.append(np.asarray(obs_tp1))
            dones.append(done)
        return (
            np.array(obses_t),
            np.array(actions),
            np.array(rewards),
            np.array(obses_tp1),
            np.array(dones),
        )

    def sample(self, batch_size):
        """Sample a batch of experiences.
        Parameters
        ----------
        batch_size: int
            How many transitions to sample.
        Returns
        -------
        obs_batch: np.array
            batch of observations
        act_batch: np.array
            batch of actions executed given obs_batch
        rew_batch: np.array
            rewards received as results of executing act_batch
        next_obs_batch: np.array
            next set of observations seen after executing act_batch
        done_mask: np.array
            done_mask[i] = 1 if executing act_batch[i] resulted in
            the end of an episode and 0 otherwise.
        """
        idxes = [random.randint(0, len(self._storage) - 1) for _ in range(batch_size)]
        return self._encode_sample(idxes)


class LazyFramesVectorReplayBuffer(ReplayBuffer):
    """
    ReplayBuffer for vectorized environments, which are wrapped into FrameBuffers.

    If an environment is first wrapped into a FrameBuffer and then vectorized,
    then the resulting VecEnv will not use LazyFrames, but it will directly
    use np.ndarrays, thus greatly increasing RAM consumption by the buffer.

    Instead, we first vectorize an environment and only then wrap in into FrameBuffers.
    It's not as convenient, but it keeps the advantage in memory from LazyFrames.

    So,
    observations and next_obervations are stored as LazyFrames
    of shape (n_frames, n_envs, ...)
    actions, rewards and dones are stored as np.ndarrays of shape (n_envs,).

    """

    # (n_frames, n_envs, *)

    def _encode_sample(self, idxes):
        """
        For each index in idxes samples a (s, a, r, s', done) transition
        from a randomly chosen environment of the corresponding VecEnv.
        """
        obses_t, actions, rewards, obses_tp1, dones = [], [], [], [], []
        for i in idxes:
            data = self._storage[i]
            obs_t, action, reward, obs_tp1, done = data
            n_envs = action.shape[0]
            env_idx_chosen_for_sample = random.randint(0, n_envs - 1)
            obses_t.append(
                np.array(obs_t, copy=False)[:, env_idx_chosen_for_sample],
            )
            actions.append(np.array(action, copy=False)[env_idx_chosen_for_sample])
            rewards.append(reward[env_idx_chosen_for_sample])
            obses_tp1.append(
                np.array(obs_tp1, copy=False)[:, env_idx_chosen_for_sample],
            )
            dones.append(done[env_idx_chosen_for_sample])
        return (
            np.array(obses_t),
            np.array(actions),
            np.array(rewards),
            np.array(obses_tp1),
            np.array(dones),
        )
