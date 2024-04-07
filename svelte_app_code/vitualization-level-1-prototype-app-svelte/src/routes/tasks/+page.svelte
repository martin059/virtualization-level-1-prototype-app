<script lang="ts">
    // ideas https://svelte.dev/examples/hello-world
    // https://colorlib.com/wp/template/responsive-table-v2/
    // sveltestrap doc https://sveltestrap.js.org/?path=%2Fdocs%2Fsveltestrap-overview--docs
    import { onMount } from 'svelte';
    import NavBar from "@components/navBar.svelte";
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
<NavBar />

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
                    <td>{new Date(task.creation_date).toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: '2-digit' })}</td>
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
    table {
        border-collapse: collapse;
    }

    th, td {
        border: 1px solid black;
        padding: 8px;
    }
</style>