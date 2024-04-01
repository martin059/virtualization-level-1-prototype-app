<script lang="ts">
    import { onMount } from 'svelte';
    interface Task {
        id: number;
        task_name: string;
        task_descrip: string;
        creation_date: Date;
        task_status: 'Created' | 'Done' | 'Deleted' | 'Dropped' | 'Postponed';
    }

    let response: any;
    let tasks: Task[] = [];

    onMount(async () => {
        try {
            const res = await fetch('http://localhost:5001/tasks');
            response = await res.json();
            tasks = response as Task[];
        } catch (error) {
            console.error(error);
        }
    });
</script>

<h1>Task List</h1>
<div>
    <table>
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
                    <td>{task.id}</td>
                    <td>{task.task_name}</td>
                    <td>{task.task_descrip}</td>
                    <td>{task.creation_date}</td>
                    <td>{task.task_status}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>

<style>
    div {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>