<script lang="ts">
    // ideas https://svelte.dev/examples/hello-world
    // https://colorlib.com/wp/template/responsive-table-v2/
    // sveltestrap doc https://sveltestrap.js.org/?path=%2Fdocs%2Fsveltestrap-overview--docs
    import { onMount } from 'svelte';
    import NavBar from "@components/navBar.svelte";
    import type { Task } from "@models/Task";

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
</script>
<NavBar />

<h1>Task List</h1>
{#if isLoading}
    <div class="loading-spinner"></div>
{:else}
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
{/if}

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

    .loading-spinner {
        border: 16px solid #f3f3f3;
        border-top: 16px solid #3498db;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        animation: spin 2s linear infinite;
        margin: auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>