<script>
    import EntriesList from "./EntriesList.svelte";
    import IntroForm from "./IntroForm.svelte";

    let step = 0;

    function nextStep() {
        step += 1;
    }

    function prevStep() {
        step -= 1;
    }

    // Gather data from the database endpoint
    let entries = [];

    async function getEntries() {
        if (false) {
            fetch('http://localhost:3000/api/entries')
                .then(res => res.json())
                .then(data => {
                    entries = data;
                });
        }
        entries = [
            { title: 'Entry 1' },
            { title: 'Entry 2' },
            { title: 'Entry 3' }
        ]
    }

    getEntries();


    // Create a variable to be mutated by a child component
    let formData = {}

    function handleSubmit(event) {
        event.preventDefault();
        console.log(formData);
        nextStep();
    }
</script>


{#await getEntries()}
    <p>Loading...</p>
{:then}
    {#if step === 0}
        <EntriesList entries={entries} />
        <button on:click={nextStep}>Next</button>
    {:else if step === 1}

        <IntroForm bind:formData={formData} handleSubmit={handleSubmit}/>

        <button on:click={prevStep}>Previous</button>
        <button on:click={nextStep}>Next</button>
    {:else}
        <p>Done!</p>
        <button on:click={prevStep}>Previous</button>
    {/if}
{:catch error}
    <p>{error.message}</p>
{/await}
