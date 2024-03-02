<script>
    export let entries;
</script>

<ul>
    {#each entries as entry}
        <li>{entry.title}</li>
    {/each}
</ul>
