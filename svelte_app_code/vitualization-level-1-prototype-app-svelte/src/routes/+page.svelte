<script lang="ts">
// @ts-nocheck
  import { Button, Col, Row } from '@sveltestrap/sveltestrap';
  import NavBar from "@components/navBar.svelte";
</script>

<main>
  <NavBar />
  <h1>Hello World to the Front end app!</h1>
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
</main>
