<script lang="ts">
// @ts-nocheck
  import {Col, Row, NavBar, Button} from "@components/commonComponents";
</script>

<main class="d-flex flex-row full-height">
  <Col class="col-1">
    <NavBar />
  </Col>
  <Col class="col-11 d-flex align-items-center flex-column">
    <h1><img src="/ToDo-icon.svg" alt="test" id="logo"> Svelte Front End ToDo App</h1>
    <p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
    <p>Find out more in the <a href="/about">About</a> section!</p>
    

    <h2>View tasks</h2>
    <p><a href="/tasks">Go to tasks view</a></p>

    <h2>Sveltestrap Test</h2>
    <Row>
      <Col>
        <Button color="primary" outline>Hello Sveltestrap!</Button>
      </Col>
    </Row>
  </Col>
</main>

<style>
  #logo {
    width: 1.75em;
    height: 1.75em;
  }
</style>