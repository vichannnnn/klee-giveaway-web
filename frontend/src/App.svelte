<script lang="ts">
  let count = 0;

  function inc() {
    count++;
  }
</script>

<main>
  <div>{count}</div>
  <button on:click={inc}>GO UP</button>
</main>

<style>

</style>