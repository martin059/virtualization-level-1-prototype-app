<script lang="ts">
  import { page } from "$app/stores";
  import { Col, NavBar, Button } from "@components/commonComponents";
  import { Notifications, acts } from "@tadashi/svelte-notification";
  import LoadingSpinner from "@components/loadingSpinner.svelte";
  import type { DueDate } from "@models/DueDate";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  // By default, the new task is created with the status 'Created'
  let newDueBy: DueDate;
  let submitEnabled: boolean = false;
  let isLoading: boolean = true;
  let taskId: string | null = $page.params.taskId;

  onMount(() => {
    // The following makes it so the initialization can be done in a consistent way in comparison with other views
    // withouth it, the form would start with empty fields for an instant and be reloaded. This way, the form is loaded fully
    newDueBy = {
      task_id: taskId,
      due_date: new Date().toISOString().split("T")[0],
      is_active: true,
    };
    submitEnabled = true;
    isLoading = false;
  });

  async function handleSubmit() {
    if (!submitEnabled) { 
      acts.add({mode: "warn",message: "Wait until a response is returned.",lifetime: 3});
      return ;
    }
    try {
      submitEnabled = false;
      const res = await fetch(
        "http://localhost:5001/tasks/" + taskId + "/due-by",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newDueBy),
          timeout: 10000, // 10 seconds
        },
      );
      const response = await res.json();
      const statusCode = res.status;
      if (statusCode >= 200 && statusCode < 300) {
        acts.add({
          mode: "success",
          message:
            "New due date created successfully. Redirecting to previous page...",
          lifetime: 2,
        });
        await new Promise((resolve) => setTimeout(resolve, 2000)); // Wait 2 seconds so user can read message
        goto("/tasks/" + taskId + "/due-by");
      } else if (statusCode == 409) {
        acts.add({
          mode: "error",
          message:
            "Due date for " +
            newDueBy.due_date +
            " already exists for this task, please either select a different one or go back to the task's due by list and activate it.",
          lifetime: 5,
        });
        console.error(
          "Due date for " +
            newDueBy.due_date +
            " already exists for this task, please either select a different one or go back to the task's due by list and activate it.",
        );
      } else {
        acts.add({
          mode: "error",
          message: "Something went wrong, for more info consult the console.",
        });
        console.error("Status response code: " + statusCode + ";Response: ");
        console.error(response);
      }
    } catch (error) {
      acts.add({
        mode: "error",
        message: "Something went wrong, for more info consult the console.",
      });
      console.error(error);
    } finally {
      submitEnabled = true;
    }
  }
</script>

<main class="d-flex flex-row full-height">
  <Col class="col-1">
    <NavBar />
  </Col>
  <Col class="col-11 d-flex align-items-center flex-column">
    <h1>New Due Date</h1>
    <Notifications />
    {#if isLoading}
      <LoadingSpinner />
    {:else}
      <Col class="col-6">
        <form on:submit|preventDefault={handleSubmit}>
          <div class="mb-3">
            <label for="task_id" class="form-label">Task ID</label>
            <input
              type="text"
              class="form-control"
              id="task_id"
              bind:value={newDueBy.task_id}
              disabled
            />
          </div>
          <div class="mb-3">
            <label for="due_date" class="form-label">Due Date</label>
            <input
              type="date"
              class="form-control"
              id="due_date"
              bind:value={newDueBy.due_date}
            />
          </div>
          <div>
            <Button type="submit" color="primary" block
              >Submit New Due date</Button
            >
          </div>
        </form>
      </Col>
    {/if}
  </Col>
</main>

<style>
  :root {
    --tadashi_svelte_notifications_width: 500px;
  }
</style>
