<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { Col, NavBar, Button } from '@components/commonComponents';
    import { Table } from '@sveltestrap/sveltestrap';
    import LoadingSpinner from '@components/loadingSpinner.svelte';
    import type { DueDate } from '@models/DueDate';
    import { Notifications, acts } from '@tadashi/svelte-notification';
    import { goto } from '$app/navigation';

    let taskId: string | null = $page.params.taskId;
    let response: any;
    let dueDates: DueDate[] = [];
    let updateInProgress: boolean = false;
    let isLoading: boolean = true;

    async function fetchData() {
        try {
            const res = await fetch('http://localhost:5001/tasks/' + taskId + '/due-by');
            const statusCode = res.status;
            response = await res.json();
            if (statusCode >= 200 && statusCode < 300) {
                dueDates = response as DueDate[];
            } else if (statusCode === 404) {
                // If the task has no due dates, the user is redirected to the task's details page
                goto('/tasks/' + taskId);
            } else {
                acts.add({mode: 'error', message: 'Something went wrong, for more info consult the console.', lifetime: 3});
                console.error('Status response code: ' + statusCode + ';Response: ');
                console.error(response);
            }
        } catch (error) {
            acts.add({ mode: 'error', message: 'Something went wrong, for more info consult the console.' });
            console.error(error);
        } finally {
            isLoading = false;
        }
    }

    onMount(fetchData);

    async function toggleDueDateActivation(toggledDueDate: DueDate) {
        if (updateInProgress) {
            acts.add({ mode: 'warn', message: 'Wait until a response is returned.', lifetime: 3});
            return;
        }
        updateInProgress = true;
        toggledDueDate.due_date = new Date(toggledDueDate.due_date)
            .toISOString()
            .split('T')[0];
        try {
            const res = await fetch( 'http://localhost:5001/tasks/' + toggledDueDate.task_id + '/due-by',
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: '{"due_date":"' + toggledDueDate.due_date + '"}',
                    timeout: 10000 // 10 seconds
                }
            );
            const response = await res.json();
            const statusCode = res.status;
            if (statusCode >= 200 && statusCode < 300) {
                let successMessage: string;
                if (toggledDueDate.is_active) {
                    successMessage = 'Due date successfully deactivated.';
                } else {
                    successMessage = 'Due date successfully activated.';
                }
                fetchData();
                acts.add({ mode: 'success', message: successMessage, lifetime: 3});
            } else {
                acts.add({mode: 'error', message: 'Something went wrong, for more info consult the console.'});
                console.error('Status response code: ' + statusCode + ';Response: ');
                console.error(response);
            }
        } catch (error) {
            acts.add({mode: 'error', message: 'Something went wrong, for more info consult the console.'});
            console.error(error);
        } finally {
            updateInProgress = false;
        }
    }

    function gotToNewDueDateForm() {
        goto('/tasks/' + taskId + '/due-by/new');
    }

    function goBack() {
        goto('/tasks/' + taskId);
    }
</script>

<main class="d-flex flex-row full-height">
    <Col class="col-1">
        <NavBar />
    </Col>
    <Col class="col-11 d-flex align-items-center flex-column">
        <div class="title-return">
            <a href="/tasks" on:click|preventDefault={goBack}
                ><img src="/left-arrow.svg" alt="Go back" class="go-back-arrow"/></a>
            <h1 class="page-title">Task {taskId}'s Due dates</h1>
        </div>
        <Notifications />
        {#if isLoading}
            <LoadingSpinner />
        {:else}
            <div class="full-height centered filling-div">
                <div class="table-div table-striped">
                    <Table striped hover>
                        <thead>
                            <tr>
                                <th>Due date</th>
                                <th>Is date active</th>
                                <th>Modify is active</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each dueDates as dueDate}
                                <tr>
                                    <td>
                                        {new Date(dueDate.due_date).toLocaleDateString(
                                            'en-GB', { year: 'numeric', month: 'long', day: '2-digit' })
                                        }
                                    </td>
                                    <td>{dueDate.is_active}</td>
                                    <td>
                                        <Button color="info" on:click={() => toggleDueDateActivation(dueDate)}>
                                        {#if dueDate.is_active}
                                            Deactivate
                                        {:else}
                                            Activate
                                        {/if}
                                        </Button>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </Table>
                    <div>
                        <Button color="primary" block on:click={() => gotToNewDueDateForm()}>Add new due date</Button>
                    </div>
                </div>
            </div>
        {/if}
    </Col>
</main>

<style>
    .filling-div {
        width: 100%;
        height: 100%;
    }
    .table-div {
        width: 90%;
    }
</style>
