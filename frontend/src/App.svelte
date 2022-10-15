<script lang="ts" xmlns="http://www.w3.org/1999/html">
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
      <html>
      <head>
        <title>Klee - Discord Bot</title>
      </head>
      <body class="landing is-preload">

      <!-- Page Wrapper -->
      <div id="page-wrapper">

        <!-- Banner -->
        <section id="banner">
          <div class="inner">
            <h2>Klee#3929</h2>
            <p>A discord bot inspired<br />
              by Genshin Impact<br />
            <ul class="actions special">
              <li><a href="https://discord.com/api/oauth2/authorize?client_id=769699482899709983&permissions=139586800704&scope=bot%20applications.commands" class="button primary" id="banner-button">Invite Me</a></li>
            <li><a href="/api/login">Log in!</a></li>
            </ul>

          </div>
          <a href="#one" class="more scrolly">Learn More</a>
        </section>

        <!-- Footer -->
        <footer id="footer">
          <ul class="icons">
            <li><a href="https://discord.gg/GFQ6DrMFQs" class="icon brands fa-discord"><span class="label">Discord</span></a></li>
            <li><a href="https://www.patreon.com/kleechann" class="icon brands fa-patreon"><span class="label">Patreon</span></a></li>
          </ul>
          <ul class="copyright">
            <li>Design: <a href="http://html5up.net">HTML5 UP</a></li>
          </ul>
        </footer>
      </div>

      <!-- Scripts -->
      <script src="assets/js/jquery.min.js"></script>
      <script src="assets/js/jquery.scrollex.min.js"></script>
      <script src="assets/js/jquery.scrolly.min.js"></script>
      <script src="assets/js/browser.min.js"></script>
      <script src="assets/js/breakpoints.min.js"></script>
      <script src="assets/js/util.js"></script>
      <script src="assets/js/main.js"></script>
      </body>
      </html>
    {/if}

    {:catch error}
      <p>Oops, we encountered an error!</p>
  {/await}
</main>

<style>

</style>