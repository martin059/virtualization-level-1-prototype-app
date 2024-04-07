<script lang="ts">
    import { Navbar, Nav, NavItem, NavLink } from '@sveltestrap/sveltestrap';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { NavObject } from '@models/NavObject';

    let routeId: string = $page.route.id ?? '';
    let activeTab: string;

    let navItems: NavObject[] = [
        new NavObject('Home', '/'),
        new NavObject('Tasks', '/tasks'),
        new NavObject('About', '/about')
    ];

    onMount(() => {
        navItems.forEach((item) => {
            if (routeId === item.href) {
                activeTab = item.label;
            }
        });
    });

    function handleTabClick(tab: string) {
        activeTab = tab;
        navItems.forEach((item) => {
            if (tab === item.label) {
                goto(item.href);
            }
        });
    }
</script>

<main>
    <Navbar color="light" light expand="md">
        <Nav tabs>
            {#each navItems as item}
                <NavItem>
                    <NavLink active={activeTab === item.label} href={item.href} on:click={() => handleTabClick(item.label)} title={item.title}>
                        {item.title}
                    </NavLink>
                </NavItem>
            {/each}
        </Nav>
    </Navbar>
</main>