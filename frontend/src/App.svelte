<script lang="ts">
  let selectedGuild = "";
  let userPromise = getUser();
  let rolePromise = getRoles(selectedGuild);

  async function getUser(): Promise<User | null> {
    try {
      const res = await fetch("/api/user");
      return await res.json() as User;
    } catch {
      return null;
    }
  }

  async function getRoles(guild_id: string) {
    try {
      const res = await fetch(`/api/guilds/${guild_id}`);
      if (res.status !== 200) return null;
      return await res.json();
    } catch {
      return null;
    }
  }

</script>

<main>
  {#await userPromise}
    Loading...
  {:then user}

    {#if user}
      Welcome {user.username}#{user.discriminator}!
      {#if user.guilds.length === 0}
        You have no common guilds! Add the bot to your server.
      {:else}
        {#each Object.entries(user.guilds) as [id, name]}
          <li>{id}: {name}</li>
        {/each}
      {/if}

    {:else}
      <div>You are not logged in.</div>
      <a href="/api/login">Log in!</a>
    {/if}

    {:catch error}
      <p>Oops, we encountered an error!</p>
  {/await}
</main>

<style>

</style>