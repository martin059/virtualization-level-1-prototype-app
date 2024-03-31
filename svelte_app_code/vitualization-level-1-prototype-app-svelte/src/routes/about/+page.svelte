<script>
    export let name = 'Svelte Front End App';
</script>

<style>
    main {
        padding: 2rem;
        text-align: center;
    }

    h1 {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    p, ul {
        font-size: 1.2rem;
    }

    ul {
        text-align: center;
        list-style-position: inside;
    }
</style>

<main>
    <h1>About { name }</h1>
    <p>Welcome to the about page of { name }! This application is meant to serve as the Front End for the main App which consist of a ToDo app.</p>
    <p>The main app is composed of three docker containers: </p>
    <ul>
        <li><strong>Postgres Container</strong>: Contains the SQL database which stores all information for the app</li>
        <li><strong>Python Container</strong>: Will serve as the Back End for the app usign Flask and Python</li>
        <li><strong>Svelte Container</strong>: Will serve as the Front End for the app using Svelte and TypeScript</li>
    </ul>
</main>