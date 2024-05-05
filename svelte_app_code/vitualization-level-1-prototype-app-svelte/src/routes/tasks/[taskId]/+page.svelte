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
    let updateDisabled: boolean = true;

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
            <Col class="col-6">
                <div>
                    <div class="mb-3">
                      <label for="task_id" class="form-label">Task ID</label>
                      <input type="text" class="form-control" id="task_id" bind:value={task.id} disabled/>
                    </div>
                    <div class="mb-3">
                      <label for="task_name" class="form-label">Task Name</label>
                      <input type="text" class="form-control" id="task_name" bind:value={task.task_name} disabled={updateDisabled}/>
                    </div>
                    <div class="mb-3">
                      <label for="task_descrip" class="form-label">Task Description</label>
                      <textarea class="form-control" id="task_descrip" rows="3" bind:value={task.task_descrip} disabled={updateDisabled}></textarea>
                    </div>
                    <div class="mb-3">
                      <label for="task_status" class="form-label">Task Status</label>
                      <select class="form-select" id="task_status" bind:value={task.task_status} disabled={updateDisabled}>
                        <option value="Created" selected>Created</option>
                        <option value="Dropped">Dropped</option>
                        <option value="Postponed">Postponed</option>
                        <option value="Done">Done</option>
                        <option value="Deleted">Deleted</option>
                      </select>
                    </div>
                </div>
            </Col>
        {/if}
    </Col>
</main>

<style>
</style>
