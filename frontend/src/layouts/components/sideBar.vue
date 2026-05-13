<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const activeIndex = computed(() => {
	if (route.path === '/profile') return '/profile'
	return '/grades'
})
</script>

<template>
	<div class="side-bar">
		<div class="brand">
			<div class="logo">SE</div>
			<div>
				<p class="brand-name">Score Query</p>
				<p class="brand-desc">学生端管理</p>
			</div>
		</div>

		<el-menu
			:default-active="activeIndex"
			class="menu"
			background-color="transparent"
			text-color="#cbd5e1"
			active-text-color="#ffffff"
			router
		>
			<el-menu-item index="/grades">成绩查询</el-menu-item>
			<el-menu-item index="/profile">学生中心</el-menu-item>
		</el-menu>
	</div>
</template>

<style scoped>
.side-bar {
	height: 100%;
	padding: 24px 16px;
}

.brand {
	display: flex;
	align-items: center;
	gap: 12px;
	margin-bottom: 28px;
}

.logo {
	width: 44px;
	height: 44px;
	display: grid;
	place-items: center;
	border-radius: 14px;
	background: linear-gradient(135deg, #2ec4b6, #5b8def);
	color: #fff;
	font-weight: 800;
}

.brand-name {
	margin: 0;
	font-size: 16px;
	font-weight: 700;
	color: #fff;
}

.brand-desc {
	margin: 2px 0 0;
	font-size: 12px;
	color: #94a3b8;
}

.menu {
	border-right: none;
}

.menu :deep(.el-menu-item) {
	height: 48px;
	border-radius: 14px;
	margin-bottom: 8px;
}

.menu :deep(.el-menu-item.is-active) {
	background: rgba(255, 255, 255, 0.12);
}
</style>
