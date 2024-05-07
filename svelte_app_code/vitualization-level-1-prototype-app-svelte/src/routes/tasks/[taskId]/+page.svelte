<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { Col, NavBar, Button } from "@components/commonComponents";
  import LoadingSpinner from "@components/loadingSpinner.svelte";
  import type { Task } from "@models/Task";
  import { Notifications, acts } from "@tadashi/svelte-notification";
  import { goto } from "$app/navigation";

  let taskId: string | null = $page.params.taskId;
  let response: any;
  let originalTask: Task;
  let task: Task;
  let isLoading: boolean = true;
  let hasDueDates: boolean = false;
  let updateDisabled: boolean = true;
  let updateInProgress: boolean = false;

  onMount(async () => {
    let dueDateChecking: boolean = false;
    try {
      const res = await fetch("http://localhost:5001/tasks/" + taskId);
      const statusCode = res.status;
      response = await res.json();
      if (statusCode >= 200 && statusCode < 300) {
        task = response[0] as Task;
        originalTask = { ...task }; // Clone task's object
        checkDueDates();
        dueDateChecking = true;
      } else {
        acts.add({
          mode: "error",
          message: "Something went wrong, for more info consult the console.",
          lifetime: 3,
        });
        console.log("Status response code: " + statusCode + ";Response: ");
        console.log(response);
      }
    } catch (error) {
      acts.add({
        mode: "error",
        message: "Something went wrong, for more info consult the console.",
        lifetime: 3,
      });
      console.error(error);
    } finally {
      // This check ensures that the proper button is displayed at the end of loading
      if (!dueDateChecking) {
        isLoading = false;
      }
    }
  });

  async function checkDueDates() {
    try {
      const res = await fetch(
        "http://localhost:5001/tasks/" + taskId + "/due-by",
      );
      const statusCode = res.status;
      if (statusCode == 404) {
        hasDueDates = false;
      } else if (statusCode == 200) {
        hasDueDates = true;
      } else {
        acts.add({
          mode: "error",
          message:
            "Something went wrong while getting task's due dates, for more info consult the console.",
          lifetime: 3,
        });
        console.log(
          "Status response code: " + statusCode + ";Response: " + response,
        );
      }
    } catch (error) {
      acts.add({
        mode: "error",
        message:
          "Something went wrong while getting task's due dates, for more info consult the console.",
        lifetime: 3,
      });
      console.error(error);
    } finally {
      isLoading = false;
    }
  }

  function gotoTaskDueDates() {
    goto("/tasks/" + taskId + "/due-by");
  }

  function createTaskDueDate() {
    goto("/tasks/" + taskId + "/due-by/new");
  }

  function toggleUpdateTask() {
    updateDisabled = !updateDisabled;
  }

  async function updateTask() {
    if (!hasTaskChanged()) {
      acts.add({ mode: "info", message: "No changes detected.", lifetime: 3 });
      return;
    }
    if (updateInProgress) {
      acts.add({
        mode: "warn",
        message: "Wait until a response is returned.",
        lifetime: 3,
      });
      return;
    }
    if (!isTaskNameValid()) {
      return;
    }
    try {
      updateInProgress = true;
      let jsonString: string = `{"task_name":"${task.task_name}","task_descrip":"${task.task_descrip}","task_status":"${task.task_status}"}`;
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
        acts.add({ mode: "success", message: "Task updated", lifetime: 3 });
        originalTask = { ...task };
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
      updateInProgress = false;
      updateDisabled = true;
    }
  }

  function isTaskNameValid(): boolean {
    if (task.task_name.trim() === "") {
      acts.add({
        mode: "error",
        message: "Task name must not be empty.",
        lifetime: 3,
      });
      return false;
    } else {
      return true;
    }
  }

  function hasTaskChanged(): boolean {
    if (
      task.task_name !== originalTask.task_name ||
      task.task_descrip !== originalTask.task_descrip ||
      task.task_status !== originalTask.task_status
    ) {
      return true;
    } else {
      return false;
    }
  }
</script>

<main class="d-flex flex-row full-height">
  <Col class="col-1">
    <NavBar />
  </Col>
  <Col class="col-11 d-flex align-items-center flex-column">
    <h1>Task Details</h1>
    <Notifications />
    {#if isLoading}
      <LoadingSpinner />
    {:else}
      <Col class="col-6">
        <div>
          <div class="mb-3">
            <label for="task_id" class="form-label">Task ID</label>
            <input
              type="text"
              class="form-control"
              id="task_id"
              bind:value={task.id}
              disabled
            />
          </div>
          <div class="mb-3">
            <label for="task_name" class="form-label">Task Name</label>
            <input
              type="text"
              class="form-control"
              id="task_name"
              bind:value={task.task_name}
              disabled={updateDisabled}
            />
          </div>
          <div class="mb-3">
            <label for="task_descrip" class="form-label">Task Description</label
            >
            <textarea
              class="form-control"
              id="task_descrip"
              rows="3"
              bind:value={task.task_descrip}
              disabled={updateDisabled}
            ></textarea>
          </div>
          <div class="mb-3">
            <label for="task_status" class="form-label">Task Status</label>
            <select
              class="form-select"
              id="task_status"
              bind:value={task.task_status}
              disabled={updateDisabled}
            >
              <option value="Created" selected>Created</option>
              <option value="Dropped">Dropped</option>
              <option value="Postponed">Postponed</option>
              <option value="Done">Done</option>
              <option value="Deleted">Deleted</option>
            </select>
          </div>
        </div>
        <div class="d-flex justify-content-between">
          {#if updateDisabled}
            <Button on:click={toggleUpdateTask} color="secondary" block
              >Enable editing</Button
            >
            <div style="margin-left: 10px;"></div>
            {#if hasDueDates}
              <Button on:click={gotoTaskDueDates} color="primary" block
                >View Task's due dates</Button
              >
            {:else}
              <Button on:click={createTaskDueDate} color="primary" block
                >Create Task's due dates</Button
              >
            {/if}
          {:else}
            <Button on:click={toggleUpdateTask} color="secondary" block
              >Cancel update</Button
            >
            <div style="margin-left: 10px;"></div>
            <Button on:click={updateTask} color="primary" block
              >Update task</Button
            >
          {/if}
        </div>
      </Col>
    {/if}
  </Col>
</main>

<style>
</style>
