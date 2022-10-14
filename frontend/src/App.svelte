<script lang="ts">
  async function getUser() {
    const res = await fetch("https://dev.himaaa.xyz/api/user");
    const json = await res.json();

    return json as User;
  }

  let userPromise = getUser();

</script>

<main>
  {#await userPromise}
    Loading...
  {:then user}
    {#if user}
      Welcome {user}!
    {:else}
      <div>You are not logged in.</div>
      <a href="https://dev.himaaa.xyz/api/login">Log in!</a>
    {/if}
  {/await}
</main>

<style>

</style>