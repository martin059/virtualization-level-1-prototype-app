<script lang="ts">
    import { onMount } from 'svelte';
    import { Col, NavBar, Button } from "@components/commonComponents";
    import { Table } from '@sveltestrap/sveltestrap';
    import LoadingSpinner from '@components/loadingSpinner.svelte';
    import { Notifications, acts } from '@tadashi/svelte-notification'
    import type { Task } from "@models/Task";
    import { goto } from '$app/navigation';

    let response: any;
    let tasks: Task[] = [];
    let isLoading: boolean = true;

    async function fetchData() {
        try {
            const res = await fetch('http://localhost:5001/tasks');
            const statusCode = res.status;
            response = await res.json();
            if (statusCode >= 200 && statusCode < 300) {
                tasks = response as Task[];
            } else {
                acts.add({ mode: 'error', message: 'Something went wrong, for more info consult the console.', lifetime: 3});
                console.log('Status response code: ' + statusCode + ';Response: ');
                console.log(response);
            }
        } catch (error) {
            acts.add({ mode: 'error', message: 'Something went wrong, for more info consult the console.' });
            console.error(error);
        } finally {
            isLoading = false;
        }
    }

    onMount(fetchData);

    function gotToNewTaskForm() {
        goto('/tasks/new');
    }

    // TODO IMPLEMENT THIS follow the example of update task
    async function updateTaskStatus(taskId: number, newStatus: string) {
        try {
          isLoading = true;
          let jsonString: string = `{"task_status":"${newStatus}"}`;
          const res = await fetch("http://localhost:5001/tasks/" + taskId, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: jsonString,
            timeout: 10000, // 10 seconds
          });
          const statusCode = await res.status;
          if (statusCode >= 200 && statusCode < 300) {
            acts.add({ mode: "success", message: "Task " + taskId + " updated", lifetime: 3 });
            fetchData();
          } else {
            const response = await res.json();
            acts.add({
              mode: "error",
              message: "Something went wrong, for more info consult the console.",
            });
            console.log("Status response code: " + statusCode + ";Response: ");
            console.log(response);
          }
        } catch (error) {
          acts.add({
            mode: "error",
            message: "Something went wrong, for more info consult the console.",
          });
          console.error(error);
        } finally {
          isLoading = false;
        }
    }

</script>

<main class="d-flex flex-row full-height">
    <Col class="col-1">
        <NavBar />
    </Col>
    <Col class="col-11 d-flex align-items-center flex-column">
        <h1>Task List</h1>
        <Notifications />
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
                                <th>Details</th>
                                <th>Actions</th>
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
                                    {#if task.task_status === 'Done' || task.task_status === 'Dropped'}
                                        <td><Button color="danger" on:click={() => updateTaskStatus(task.id, 'Deleted')}>Delete</Button></td>
                                    {:else if task.task_status !== 'Deleted'}
                                        <td>
                                            <Button color="success" on:click={() => updateTaskStatus(task.id, 'Done')}>Done</Button>
                                            <Button color="warning" on:click={() => updateTaskStatus(task.id, 'Dropped')}>Drop</Button>
                                        </td>
                                    {:else}
                                    <td><Button color="secondary" disabled>N/A</Button></td>
                                    {/if}
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