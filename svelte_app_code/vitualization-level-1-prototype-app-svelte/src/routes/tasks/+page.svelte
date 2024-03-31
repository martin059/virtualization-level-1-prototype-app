<script lang="ts">
    import { onMount } from 'svelte';
    interface Task {
        id: number;
        task_name: string;
        task_descrip: string;
        creation_date: string;
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

<ul>
    {#each tasks as task (task.id)}
        <li>{task.id} - {task.task_name} - {task.task_descrip} - {task.creation_date} - {task.task_status}</li>
    {/each}
</ul>