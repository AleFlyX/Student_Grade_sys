-- ==========================================
-- 解决中文乱码：先设置字符集
-- ==========================================
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 删除旧数据库（如果存在且需要重建）
DROP DATABASE IF EXISTS grade_system;

-- 创建数据库（明确指定字符集）
CREATE DATABASE grade_system
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE grade_system;

-- ==========================================
-- 1. 学生表
-- ==========================================
CREATE TABLE `students` (
  `student_id` VARCHAR(20) PRIMARY KEY COMMENT '学号',
  `name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
  `major` VARCHAR(100) COMMENT '专业',
  `grade` VARCHAR(20) COMMENT '年级',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生信息表';

-- ==========================================
-- 2. 课程表
-- ==========================================
CREATE TABLE `courses` (
  `course_id` VARCHAR(20) PRIMARY KEY COMMENT '课程编号',
  `course_name` VARCHAR(100) NOT NULL COMMENT '课程名称',
  `credit` DECIMAL(3,1) NOT NULL COMMENT '学分',
  `course_nature` VARCHAR(20) NOT NULL COMMENT '课程性质'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程信息表';

-- ==========================================
-- 3. 成绩表
-- ==========================================
CREATE TABLE `grades` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` VARCHAR(20) NOT NULL COMMENT '学号',
  `course_id` VARCHAR(20) NOT NULL COMMENT '课程编号',
  `academic_year` VARCHAR(10) NOT NULL COMMENT '学年',
  `semester` ENUM('AUTUMN','SPRING','SUMMER') NOT NULL COMMENT '学期',
  `score` DECIMAL(5,1) NOT NULL CHECK (score >= 0 AND score <= 100),
  `status` VARCHAR(20) DEFAULT '正常' COMMENT '成绩状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`student_id`) REFERENCES `students`(`student_id`) ON DELETE CASCADE,
  FOREIGN KEY (`course_id`) REFERENCES `courses`(`course_id`) ON DELETE CASCADE,
  UNIQUE KEY `uk_student_course_semester` (`student_id`, `course_id`, `academic_year`, `semester`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生成绩表';

-- ==========================================
-- 插入测试数据（使用 UTF8 编码）
-- ==========================================
-- 密码均为 '123456' 的 SHA256 哈希
INSERT INTO `students` (`student_id`, `name`, `password_hash`, `major`, `grade`) VALUES
('2021001234', '张三', SHA2('123456', 256), '计算机科学与技术', '2021级'),
('2021005678', '李四', SHA2('123456', 256), '软件工程', '2021级'),
('2022009876', '王芳', SHA2('123456', 256), '数据科学与大数据技术', '2022级'),
('2023001122', '赵伟', SHA2('123456', 256), '人工智能', '2023级'),
('2023003344', '陈思琪', SHA2('123456', 256), '计算机科学与技术', '2023级');

INSERT INTO `courses` (`course_id`, `course_name`, `credit`, `course_nature`) VALUES
('CS101', '程序设计基础', 3.5, '必修'),
('CS201', '数据结构', 4.0, '必修'),
('CS301', '数据库原理', 3.5, '必修'),
('MA102', '高等数学A', 5.0, '必修'),
('MA203', '线性代数', 2.5, '必修'),
('EE205', '大学物理', 3.0, '必修'),
('PE001', '大学体育', 1.0, '必修'),
('GE009', '中华文化概论', 2.0, '选修'),
('CS401', '机器学习基础', 3.0, '选修'),
('GE101', '艺术鉴赏', 2.0, '选修');

INSERT INTO `grades` (`student_id`, `course_id`, `academic_year`, `semester`, `score`, `status`) VALUES
-- 张三（2021001234）的成绩
('2021001234', 'CS101', '2024-2025', 'AUTUMN', 88.5, '正常'),
('2021001234', 'MA102', '2024-2025', 'AUTUMN', 72.0, '正常'),
('2021001234', 'PE001', '2024-2025', 'AUTUMN', 95.0, '正常'),
('2021001234', 'CS201', '2024-2025', 'SPRING', 78.0, '正常'),
('2021001234', 'EE205', '2024-2025', 'SPRING', 65.0, '正常'),
('2021001234', 'GE009', '2024-2025', 'SPRING', 85.0, '正常'),
('2021001234', 'CS301', '2025-2026', 'AUTUMN', 82.0, '正常'),

-- 李四（2021005678）的成绩
('2021005678', 'CS101', '2024-2025', 'AUTUMN', 92.0, '正常'),
('2021005678', 'MA102', '2024-2025', 'AUTUMN', 68.0, '正常'),
('2021005678', 'PE001', '2024-2025', 'AUTUMN', 88.0, '正常'),
('2021005678', 'CS201', '2024-2025', 'SPRING', 85.5, '正常'),
('2021005678', 'GE009', '2024-2025', 'SPRING', 78.5, '正常'),

-- 王芳（2022009876）的成绩（含补考）
('2022009876', 'CS101', '2025-2026', 'AUTUMN', 72.0, '正常'),
('2022009876', 'MA102', '2025-2026', 'AUTUMN', 55.0, '正常'),
('2022009876', 'MA102', '2025-2026', 'SPRING', 68.0, '补考'),
('2022009876', 'PE001', '2025-2026', 'AUTUMN', 90.0, '正常'),
('2022009876', 'CS201', '2025-2026', 'SPRING', 76.5, '正常'),

-- 赵伟（2023001122）的成绩
('2023001122', 'CS101', '2025-2026', 'AUTUMN', 85.0, '正常'),
('2023001122', 'MA102', '2025-2026', 'AUTUMN', 91.0, '正常'),
('2023001122', 'MA203', '2025-2026', 'AUTUMN', 88.0, '正常'),
('2023001122', 'PE001', '2025-2026', 'AUTUMN', 92.0, '正常'),
('2023001122', 'GE101', '2025-2026', 'AUTUMN', 95.0, '选修'),

-- 陈思琪（2023003344）的成绩
('2023003344', 'CS101', '2025-2026', 'AUTUMN', 94.0, '正常'),
('2023003344', 'MA102', '2025-2026', 'AUTUMN', 87.5, '正常'),
('2023003344', 'MA203', '2025-2026', 'AUTUMN', 84.0, '正常'),
('2023003344', 'PE001', '2025-2026', 'AUTUMN', 96.0, '正常');

SET FOREIGN_KEY_CHECKS = 1;

-- ==========================================
-- 验证数据是否正常显示
-- ==========================================
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM grades LIMIT 10;