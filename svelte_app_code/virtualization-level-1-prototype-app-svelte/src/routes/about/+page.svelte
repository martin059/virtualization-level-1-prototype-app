<script lang="ts">
    // @ts-ignore
    import { Col, NavBar } from '@components/commonComponents';
    export let name: string = 'Svelte Front End App';
    import { goto } from '$app/navigation';

    function goBack() {
        goto('/');
    }
</script>

<main class="d-flex flex-row full-height">
    <Col class="col-1">
        <NavBar />
    </Col>
    <Col class="col-11 d-flex align-items-center flex-column">
        <div class="title-return">
            <a href="/tasks" on:click|preventDefault={goBack}><img src="/left-arrow.svg" alt="Go back" class="go-back-arrow"/></a>
            <h1 class="page-title">About { name }</h1>
        </div>
        <div class="full-height centered-vertical increased-txt-size">
            <p>Welcome to the <strong>About page of { name }!</strong>.</p>
            <p>This application is meant to serve as the Front End for the main App which consist of a simple ToDo app.</p>
            <p>The main app is composed of three <a href="https://www.docker.com/"><img src="/docker-whale.svg" alt="Docker logo" class="about-logo text-logo"></a><strong>Docker</strong> containers:</p>
            <ul>
                <li>
                    <a href="https://www.postgresql.org/"><img src="/Postgresql_elephant.svg" alt="PostgreSQL logo" class="about-logo"></a> 
                    <strong>Postgres Container</strong>: It contains the SQL database which stores all information for the app.
                </li>
                <li>
                    <a href="https://www.python.org/"><img src="/Python-logo.svg" alt="Python logo" class="about-logo"></a>
                    <strong>Python Container</strong>: It serves as the Back End for the app usign Python and <a href="https://flask.palletsprojects.com/"><img src="/flask.svg" alt="Flask logo" class="about-logo text-logo"></a> Flask.
                </li>
                <li>
                    <a href="https://svelte.dev/"><img src="/Svelte_Logo.svg" alt="Svelte logo" class="about-logo"></a>
                    <strong>Svelte Container</strong>: It serves as the Front End for the app using Svelte, <a href="https://www.typescriptlang.org/"><img src="/Typescript.svg" alt="TypeScript logo" class="about-logo text-logo"></a> TypeScript and Sveltestrap.
                </li>
            </ul>
            <p>This entire containerized web app was developed in a Linux virtual machine using the <a href="https://manjaro.org/"><img src="/manjaro-logo.svg" alt="Manjaro logo" class="about-logo text-logo"></a> Manjaro distro. It was later compiled and tested in an <a href="https://almalinux.org/"><img src="/AlmaLinux_Icon_Logo.svg" alt="AlmaLinux logo" class="about-logo text-logo"></a> AlmaLinux 9 setup with <a href="https://www.vagrantup.com/"><img src="/vagrant.svg" alt="Vagrant logo" class="about-logo text-logo"></a> Vagrant and configured using an <a href="https://www.ansible.com/"><img src="/ansible.svg" alt="Ansible logo" class="about-logo text-logo"></a> Ansible script.</p>
        </div>
    </Col>
</main>

<style>
    .about-logo {
        width: 1.75em;
        height: 1.75em;
        margin-right: .2em;
    }
    .text-logo {
        margin-left: .2em;
    }
    .increased-txt-size {
        font-size: 1.2em;
    }
</style>