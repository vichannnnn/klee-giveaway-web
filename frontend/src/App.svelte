<script lang="ts">
  // import {memberMock, nulLMemberMock, nullRoleMock, roleMock, userMock} from "./mocks";

  let selectedGuild = "";
  let selectedRole = "";

  let userPromise = getUser();
  let rolePromise = getRoles(selectedGuild);
  let memberPromise = getMembers(selectedGuild, selectedRole);

  async function getUser(): Promise<User | null> {
    try {

      const res = await fetch("/api/user");
      return await res.json() as User;

      //return userMock;
    } catch {
      return null;
    }
  }

  async function getRoles(guild_id: string): Promise<RoleList | null> {
    try {

      const res = await fetch(`/api/guilds/${guild_id}`);
      if (res.status !== 200) return null;
      return await res.json();

      // if (guild_id === "660135595250810881") return roleMock
      // else return nullRoleMock;
    } catch {
      return null;
    }
  }

  async function getMembers(guild_id: string, role_id: string): Promise<MemberList | null> {
    try {

      const res = await fetch(`/api/guilds/${guild_id}/${role_id}`);
      if (res.status !== 200) return null;
      return await res.json();

      // if (role_id === "1007736912246738965") return memberMock;
      // else return nulLMemberMock;
    } catch {
      return null;
    }
  }

  function updateSelectedGuild(): void {
    rolePromise = getRoles(selectedGuild);
  }

  function updateSelectedMembers(): void {
    memberPromise = getMembers(selectedGuild, selectedRole);
  }

</script>

<main>
  {#await userPromise}
    Loading...
  {:then user}

    {#if user}
      Welcome {user.username}#{user.discriminator}!
      {#if Object.values(user.guilds).length === 0}
        You have no common guilds! Add the bot to your server.
      {:else}
        Selected Guild: {selectedGuild}
        {#each Object.entries(user.guilds) as [id, name]}
          <li class="text-red-500" on:click={() => {selectedGuild = id; updateSelectedGuild()}}>{id}: {name}</li>
        {/each}

        {#if selectedGuild !== ""}
          <div on:click={() => {selectedGuild = ""; selectedRole = ""}}>Back</div>
          {#await rolePromise}
            Loading roles...
          {:then roles}
            Selected Role: {selectedRole}
            {#each Object.entries(roles) as [id, name]}
              <li class="text-green-800" on:click={() => {selectedRole = id; updateSelectedMembers()}}>{id}: {name}</li>
            {/each}

            {#if selectedRole !== ""}
              <div on:click={() => {selectedRole = ""}}>Back</div>
              {#await memberPromise}
                Loading members...
              {:then members}
                {#each Object.entries(members) as [id, data]}
                  <li class="text-blue-500">{id}: {data}</li>
                {/each}
              {/await}
            {/if}
          {/await}
        {/if}

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