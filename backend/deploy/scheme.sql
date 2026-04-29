-- 创建数据库（可选，根据实际情况调整）
CREATE DATABASE IF NOT EXISTS grade_system
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE grade_system;

-- ----------------------------
-- 1. 学生表
-- ----------------------------
CREATE TABLE `students` (
  `student_id` VARCHAR(20) PRIMARY KEY COMMENT '学号',
  `name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希（SHA256或bcrypt）',
  `major` VARCHAR(100) COMMENT '专业',
  `grade` VARCHAR(20) COMMENT '年级，如“2021级”',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';

-- ----------------------------
-- 2. 课程表
-- ----------------------------
CREATE TABLE `courses` (
  `course_id` VARCHAR(20) PRIMARY KEY COMMENT '课程编号',
  `course_name` VARCHAR(100) NOT NULL COMMENT '课程名称',
  `credit` DECIMAL(3,1) NOT NULL COMMENT '学分',
  `course_nature` VARCHAR(20) NOT NULL COMMENT '课程性质：必修/选修/公选'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程信息表';

-- ----------------------------
-- 3. 成绩表
-- ----------------------------
CREATE TABLE `grades` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` VARCHAR(20) NOT NULL COMMENT '学号',
  `course_id` VARCHAR(20) NOT NULL COMMENT '课程编号',
  `academic_year` VARCHAR(10) NOT NULL COMMENT '学年，如“2024-2025”',
  `semester` ENUM('AUTUMN','SPRING','SUMMER') NOT NULL COMMENT '学期',
  `score` DECIMAL(5,1) NOT NULL CHECK (score >= 0 AND score <= 100) COMMENT '总评成绩',
  `status` VARCHAR(20) DEFAULT '正常' COMMENT '成绩状态：正常/补考/重修',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`student_id`) REFERENCES `students`(`student_id`) ON DELETE CASCADE,
  FOREIGN KEY (`course_id`) REFERENCES `courses`(`course_id`) ON DELETE CASCADE,
  UNIQUE KEY `uk_student_course_semester` (`student_id`, `course_id`, `academic_year`, `semester`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生成绩表';