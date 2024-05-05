<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { Col, NavBar, Button } from "@components/commonComponents";
    import { Table } from '@sveltestrap/sveltestrap';
    import LoadingSpinner from '@components/loadingSpinner.svelte';
    import type { DueDate } from "@models/DueDate";
    import { Notifications, acts } from '@tadashi/svelte-notification'
    // import { goto } from '$app/navigation';

    let taskId: string | null = $page.params.taskId;
    let response: any;
    let dueDates: DueDate[] = [];
    let isLoading: boolean = true;

    onMount(async () => {
        try {
            const res = await fetch('http://localhost:5001/tasks/' + taskId + '/due-by');
            const statusCode = res.status;
            response = await res.json();
            if (statusCode >= 200 && statusCode < 300) {
                dueDates = response as DueDate[];
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
    });

    function gotToNewDueDateForm() {
        acts.add({ mode: 'warn', message: 'To be implemented', lifetime: 3});
        // goto('/tasks/' + taskId + '/due-by/new'); // TODO implement this
    }

</script>

<main class="d-flex flex-row full-height">
    <Col class="col-1">
        <NavBar />
    </Col>
    <Col class="col-11 d-flex align-items-center flex-column">
        <h1>Task {taskId}'s Due dates</h1>
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
                            {#each dueDates as dueDate }
                                <tr>
                                    <td>{new Date(dueDate.due_date).toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: '2-digit' })}</td>
                                    <td>{dueDate.is_active}</td>
                                    {#if dueDate.is_active}
                                        <td><Button color="info" on:click={() => acts.add({ mode: 'warn', message: 'To be implemented', lifetime: 3})}>Deactivate</Button></td>
                                    {:else}
                                        <td><Button color="info" on:click={() => acts.add({ mode: 'warn', message: 'To be implemented', lifetime: 3})}>Activate</Button></td>
                                    {/if}
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
    .filling-div { width: 100%;height: 100%;}
    .table-div { width: 90%; }
</style>