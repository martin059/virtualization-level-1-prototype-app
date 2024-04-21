<script lang="ts">
    import { page } from '$app/stores';
    import NavBar from "@components/navBar.svelte";

    let taskId: string | null = $page.params.taskId;
</script>
<NavBar />
<main>
    <h1>Task Details</h1>
    <p>Task ID: {taskId}</p>
    <!-- Add more details about the task here -->
</main>

<style>
    /* Add your styles here */
</style>
