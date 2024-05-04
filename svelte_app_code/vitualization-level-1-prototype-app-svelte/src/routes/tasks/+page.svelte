<script lang="ts">
    import { onMount } from 'svelte';
    import { Col, NavBar, Button } from "@components/commonComponents";
    import { Table } from '@sveltestrap/sveltestrap';
    import LoadingSpinner from '@components/loadingSpinner.svelte';
    import type { Task } from "@models/Task";
    import { goto } from '$app/navigation';

    let response: any;
    let tasks: Task[] = [];
    let isLoading = true;

    onMount(async () => {
        try {
            const res = await fetch('http://localhost:5001/tasks');
            response = await res.json();
            tasks = response as Task[];
        } catch (error) {
            console.error(error);
        } finally {
            isLoading = false;
        }
    });

    function gotToNewTaskForm() {
        goto('/tasks/new');
    }
</script>

<main class="d-flex flex-row full-height">
    <Col class="col-1">
        <NavBar />
    </Col>
    <Col class="col-11 d-flex align-items-center flex-column">
        <h1>Task List</h1>
        {#if isLoading}
            <LoadingSpinner />
        {:else}
            <div class="full-height centered filling-div">
                <div class="table-div table-striped">
                    <Table striped hover>
                        <thead>
                            <tr>
                                <th>Id</th>
                                <th>Name</th>
                                <th>Description</th>
                                <th>Creation Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each tasks as task (task.id)}
                                <tr>
                                    <th scope="row">{task.id}</th>
                                    <td>{task.task_name}</td>
                                    <td>{task.task_descrip}</td>
                                    <td>{new Date(task.creation_date).toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: '2-digit' })}</td>
                                    <td>{task.task_status}</td>
                                    <td><Button color="info" on:click={() => goto(`/tasks/${task.id}`)}>View</Button></td>
                                </tr>
                            {/each}
                        </tbody>
                    </Table>
                    <div>
                        <Button color="primary" block on:click={() => gotToNewTaskForm()}>Create new Task</Button>
                    </div>
                </div>
            </div>
        {/if}
    </Col>
</main>

<style>
    .filling-div { width: 100%;height: 100%;}
    .table-div { width: 90%; }
</style>