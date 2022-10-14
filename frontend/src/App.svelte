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
    {:else}
      <div>You are not logged in.</div>
      <a href="https://dev.himaaa.xyz/api/login">Log in!</a>
    {/if}
  {/await}
</main>

<style>

</style>