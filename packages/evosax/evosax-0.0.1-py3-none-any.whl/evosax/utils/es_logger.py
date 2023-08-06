import pickle
import jax
import jax.numpy as jnp
from functools import partial
import matplotlib.pyplot as plt


class ESLog(object):
    def __init__(self, num_dims: int, num_generations: int, top_k: int):
        self.num_dims = num_dims
        self.num_generations = num_generations
        self.top_k = top_k

    @partial(jax.jit, static_argnums=(0,))
    def initialize(self):
        log = {
            "top_fitness": jnp.zeros(self.top_k) + 1e10,
            "top_params": jnp.zeros((self.top_k, self.num_dims)),
            "log_top_1": jnp.zeros(self.num_generations),
            "log_top_mean": jnp.zeros(self.num_generations),
            "log_top_std": jnp.zeros(self.num_generations),
            "log_gen_1": jnp.zeros(self.num_generations),
            "log_gen_mean": jnp.zeros(self.num_generations),
            "log_gen_std": jnp.zeros(self.num_generations),
            "gen_counter": 0,
        }
        return log

    @partial(jax.jit, static_argnums=(0,))
    def update(self, log, x, fitness):
        # Check if there are solutions better than current archive
        vals = jnp.hstack([log["top_fitness"], fitness])
        params = jnp.vstack([log["top_params"], x])
        top_idx = vals.argsort()
        log["top_fitness"] = vals[top_idx[: self.top_k]]
        log["top_params"] = params[top_idx[: self.top_k]]
        log["log_top_1"] = jax.ops.index_update(
            log["log_top_1"], log["gen_counter"], log["top_fitness"][0]
        )
        log["log_top_mean"] = jax.ops.index_update(
            log["log_top_mean"], log["gen_counter"], jnp.mean(log["top_fitness"])
        )
        log["log_top_std"] = jax.ops.index_update(
            log["log_top_std"], log["gen_counter"], jnp.std(log["top_fitness"])
        )
        log["log_gen_1"] = jax.ops.index_update(
            log["log_gen_1"], log["gen_counter"], jnp.min(fitness)
        )
        log["log_gen_mean"] = jax.ops.index_update(
            log["log_gen_mean"], log["gen_counter"], jnp.mean(fitness)
        )
        log["log_gen_std"] = jax.ops.index_update(
            log["log_gen_std"], log["gen_counter"], jnp.std(fitness)
        )
        log["gen_counter"] += 1
        return log

    def save(self, log, filename):
        """Save different parts of logger in .pkl file."""
        with open(filename, "wb") as handle:
            pickle.dump(log, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        """Reload the pickle logger and return dictionary."""
        with open(filename, "rb") as handle:
            es_logger = pickle.load(handle)
        return es_logger

    def plot(
        self,
        log,
        title,
        ylims=None,
        fig=None,
        ax=None,
        no_legend=False,
    ):
        """Plot fitness trajectory from evo logger over generations."""
        if fig is None or ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(6, 3))
        int_range = jnp.arange(1, log["gen_counter"] + 1)
        ax.plot(int_range, log["log_top_1"][: log["gen_counter"]], label="Top 1")
        ax.plot(
            int_range,
            log["log_top_mean"][: log["gen_counter"]],
            label=f"Top-{self.top_k} Mean",
        )
        ax.plot(int_range, log["log_gen_1"][: log["gen_counter"]], label="Gen. 1")
        ax.plot(int_range, log["log_gen_mean"][: log["gen_counter"]], label="Gen. Mean")
        if ylims is not None:
            ax.set_ylim(ylims)
        if not no_legend:
            ax.legend()
        if title is not None:
            ax.set_title(title)
        ax.set_xlabel("Number of Generations")
        ax.set_ylabel("Fitness Score")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        return fig, ax
