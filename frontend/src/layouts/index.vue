<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import HeadBar from './components/headBar.vue'
import SideBar from './components/sideBar.vue'

const route = useRoute()
const userStore = useUserStore()

const student = computed(() => userStore.studentInfo)
const contentClass = computed(() => ({ 'is-auth-page': route.meta.requiresAuth !== false }))
</script>

<template>
	<el-container class="layout-shell">
		<el-aside class="layout-sider" width="220px">
			<SideBar />
		</el-aside>

		<el-container class="layout-main">
			<el-header class="layout-header" height="72px">
				<HeadBar :student="student" />
			</el-header>

			<el-main :class="['layout-content', contentClass]">
				<RouterView />
			</el-main>
		</el-container>
	</el-container>
</template>

<style scoped>
.layout-shell {
	min-height: 100vh;
	background:
		radial-gradient(circle at top left, rgba(46, 196, 182, 0.08), transparent 28%),
		linear-gradient(180deg, #f7fafc 0%, #eef4f8 100%);
}

.layout-sider {
	background: linear-gradient(180deg, #0f172a 0%, #132238 100%);
	color: #fff;
	box-shadow: 8px 0 24px rgba(15, 23, 42, 0.12);
}

.layout-main {
	min-width: 0;
}

.layout-header {
	padding: 0;
	background: rgba(255, 255, 255, 0.82);
	backdrop-filter: blur(18px);
	border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.layout-content {
	min-height: calc(100vh - 72px);
	padding: 24px;
}

@media (max-width: 960px) {
	.layout-sider {
		display: none;
	}

	.layout-content {
		padding: 16px;
	}
}
</style>
