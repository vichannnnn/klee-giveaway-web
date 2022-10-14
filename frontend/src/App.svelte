<script lang="ts">
  async function getUser(): Promise<User | null> {
    const res = await fetch("https://dev.himaaa.xyz/api/user");
    if (res.status !== 200) return null;
    const json = await res.json();

    return json as User;
  }

  let userPromise = getUser();

</script>

<main>
  {#await userPromise}
    Loading...
  {:then user}

    {#if user !== null}
      Welcome {user.username}#{user.discriminator}!
      {#if user.guilds.length === 0}
        You have no common guilds! Add the bot to your server.
      {:else}
        {#each Array(user.guilds.entries) as entry}
          <li>{entry}</li>
        {/each}
      {/if}

    {:else}
      <div>You are not logged in.</div>
      <a href="https://dev.himaaa.xyz/api/login">Log in!</a>
    {/if}

  {/await}
</main>

<style>

</style>