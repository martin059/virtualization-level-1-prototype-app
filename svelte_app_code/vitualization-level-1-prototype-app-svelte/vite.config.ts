import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import alias from '@rollup/plugin-alias';

export default defineConfig({
	plugins: [
		sveltekit(),
		alias({
			entries: [
				{ find: '@components', replacement: 'src/components' }
			]
		})
	]
});
