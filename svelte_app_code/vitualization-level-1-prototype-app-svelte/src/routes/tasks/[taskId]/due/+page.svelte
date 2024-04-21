<script lang="ts">
    import NavBar from "@components/navBar.svelte";
    import { page } from '$app/stores';

    let taskId: string | null = $page.params.taskId;
</script>
<NavBar />
<main>
    <h1>Task Due dates</h1>
    <p>Due dates for Task ID: {taskId}</p>
    <!-- Add more details about the task here -->
</main>

<style>
    /* Add your styles here */
</style>
