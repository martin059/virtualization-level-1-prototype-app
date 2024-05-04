<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { Col, NavBar, Button } from "@components/commonComponents";
    import LoadingSpinner from '@components/loadingSpinner.svelte';
    import type { Task } from "@models/Task";
    import { Notifications, acts } from '@tadashi/svelte-notification'
    import { goto } from '$app/navigation';

    let taskId: string | null = $page.params.taskId;
    let response: any;
    let task: Task;
    let isLoading: boolean = true;

    onMount(async () => {
        try {
            const res = await fetch('http://localhost:5001/tasks/' + taskId);
            const statusCode = res.status;
            if (statusCode >= 200 && statusCode < 300) {
                response = await res.json();
                task = response[0] as Task;
            } else {
                acts.add({ mode: 'error', message: 'Something went wrong, for more info consult the console.', lifetime: 3});
                console.log(response);
            }
        } catch (error) {
            acts.add({ mode: 'error', message: 'Something went wrong, for more info consult the console.', lifetime: 3 });
            console.error(error);
        } finally {
            isLoading = false;
        }
    });
</script>

<main class="d-flex flex-row full-height">
    <Col class="col-1">
        <NavBar />
    </Col>
    <Col class="col-11 d-flex align-items-center flex-column">
        <h1>Task Details</h1>
        <Notifications />
        {#if isLoading}
            <LoadingSpinner />
        {:else}
            <p>Task ID: {task.id}</p>
            <p>Task Name: {task.task_name}</p>
            <p>Task Description: {task.task_descrip}</p>
            <p>Task Status: {task.task_status}</p>
        {/if}
    </Col>
</main>

<style>
</style>
