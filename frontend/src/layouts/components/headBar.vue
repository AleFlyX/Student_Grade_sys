<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { logoutApi } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const props = defineProps<{
	student: { name: string } | null
}>()

const router = useRouter()
const userStore = useUserStore()

const avatarLetter = computed(() => props.student?.name?.slice(0, 1) || 'S')

const goProfile = () => {
	router.push('/profile#profile-info')
}

const goEditProfile = () => {
	router.push('/profile#profile-edit')
}

const logout = async () => {
	try {
		await logoutApi()
	} catch {
		// token 失效时直接本地退出
	}
	userStore.clearUser()
	ElMessage.success('已退出登录')
	router.push('/login')
}
</script>

<template>
	<div class="head-bar">
		<div class="title-block">
			<p class="eyebrow">University Score System</p>
			<h2>学生成绩管理平台</h2>
		</div>

		<div class="actions">
			<el-dropdown trigger="click">
				<div class="avatar-trigger">
					<el-avatar :size="40" class="avatar">{{ avatarLetter }}</el-avatar>
					<div class="meta">
						<span class="name">{{ student?.name || '未登录' }}</span>
						<span class="hint">个人中心</span>
					</div>
					<el-icon class="chevron"><ArrowDown /></el-icon>
				</div>

				<template #dropdown>
					<el-dropdown-menu>
						<el-dropdown-item @click="goProfile">个人信息</el-dropdown-item>
						<el-dropdown-item @click="goEditProfile">修改个人信息</el-dropdown-item>
						<el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
					</el-dropdown-menu>
				</template>
			</el-dropdown>
		</div>
	</div>
</template>

<style scoped>
.head-bar {
	height: 72px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 0 24px;
}

.title-block h2 {
	margin: 2px 0 0;
	font-size: 20px;
	color: #102a43;
}

.eyebrow {
	margin: 0;
	font-size: 12px;
	letter-spacing: 2px;
	text-transform: uppercase;
	color: #7c8aa0;
}

.avatar-trigger {
	display: flex;
	align-items: center;
	gap: 12px;
	cursor: pointer;
	padding: 6px 10px;
	border-radius: 999px;
	transition: background 0.2s ease;
}

.avatar-trigger:hover {
	background: rgba(15, 23, 42, 0.04);
}

.avatar {
	background: linear-gradient(135deg, #2ec4b6, #5b8def);
	color: #fff;
	font-weight: 700;
}

.meta {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	line-height: 1.1;
}

.name {
	font-weight: 700;
	color: #102a43;
}

.hint {
	font-size: 12px;
	color: #7c8aa0;
}

.chevron {
	color: #52606d;
}

@media (max-width: 768px) {
	.head-bar {
		padding: 0 16px;
	}

	.title-block {
		display: none;
	}

	.meta {
		display: none;
	}
}
</style>
