<script lang="ts">
    // @ts-ignore
    import {Col, NavBar} from "@components/commonComponents";
    export let name: string = 'Svelte Front End App';
</script>

<main class="d-flex flex-row full-height">
    <Col class="col-1">
        <NavBar />
    </Col>
    <Col class="col-11 d-flex align-items-center flex-column">
        <h1 class="page-title">About { name }</h1>
        <p>Welcome to the about page of { name }! This application is meant to serve as the Front End for the main App which consist of a ToDo app.</p>
        <p>The main app is composed of three docker containers: </p>
        <ul>
            <li><strong>Postgres Container</strong>: Contains the SQL database which stores all information for the app</li>
            <li><strong>Python Container</strong>: Will serve as the Back End for the app usign Flask and Python</li>
            <li><strong>Svelte Container</strong>: Will serve as the Front End for the app using Svelte and TypeScript</li>
        </ul>
    </Col>
</main>