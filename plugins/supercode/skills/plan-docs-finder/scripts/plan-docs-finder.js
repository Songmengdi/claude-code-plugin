#!/usr/bin/env node

/**
 * Plan Docs Finder
 * 扫描 docs/plans 目录提取所有文档的 frontmatter 元数据
 *
 * 用法: node plan-docs-finder.js <plans_directory>
 * 示例: node plan-docs-finder.js /path/to/project/docs/plans
 */

const fs = require('fs');
const path = require('path');

// 获取命令行参数
const args = process.argv.slice(2);

if (args.length === 0) {
    console.error('错误: 请指定 docs/plans 目录的绝对路径');
    console.error('用法: node plan-docs-finder.js <plans_directory>');
    console.error('示例: node plan-docs-finder.js /path/to/project/docs/plans');
    process.exit(1);
}

const PLANS_DIR = path.resolve(args[0]);

// 检查目录是否存在
if (!fs.existsSync(PLANS_DIR)) {
    console.log('[]');
    process.exit(0);
}

// 解析 frontmatter
function parseFrontmatter(content) {
    const lines = content.split('\n');
    const result = {};
    let inFrontmatter = false;
    let i = 0;

    // 查找 frontmatter 开始
    while (i < lines.length) {
        if (lines[i].trim() === '---') {
            inFrontmatter = true;
            i++;
            break;
        }
        i++;
    }

    if (!inFrontmatter) return null;

    // 解析 frontmatter 内容
    while (i < lines.length) {
        const line = lines[i];
        const trimmed = line.trim();

        if (trimmed === '---') break;

        if (trimmed && !trimmed.startsWith('#')) {
            const colonIndex = trimmed.indexOf(':');

            if (colonIndex !== -1) {
                const key = trimmed.slice(0, colonIndex).trim();
                const value = trimmed.slice(colonIndex + 1).trim();

                // 检查下一行是否有子属性（缩进）
                if (i + 1 < lines.length) {
                    const nextLine = lines[i + 1];
                    const nextIndent = nextLine.match(/^\s*/)[0].length;
                    const currentIndent = line.match(/^\s*/)[0].length;

                    // 下一行缩进更深，说明有子属性（YAML 列表格式）
                    if (nextIndent > currentIndent && nextLine.trim()) {
                        const subProps = {};
                        let j = i + 1;

                        while (j < lines.length) {
                            const subLine = lines[j];
                            const subTrimmed = subLine.trim();

                            if (!subTrimmed || subTrimmed === '---') break;

                            const subIndent = subLine.match(/^\s*/)[0].length;
                            if (subIndent <= currentIndent) break;

                            // 解析列表项: - key: value
                            const match = subTrimmed.match(/^-\s*(\w+):\s*(.+)$/);
                            if (match) {
                                subProps[match[1]] = match[2];
                            }

                            j++;
                        }

                        result[key] = subProps;
                        i = j - 1; // 跳过已处理的子行
                    } else {
                        // 简单键值对
                        result[key] = parseValue(value);
                    }
                } else {
                    result[key] = parseValue(value);
                }
            }
        }
        i++;
    }

    return result;
}

// 解析值（处理数组、字符串等）
function parseValue(value) {
    if (!value) return '';
    // 解析数组 [item1, item2]
    if (value.startsWith('[') && value.endsWith(']')) {
        return value.slice(1, -1)
            .split(',')
            .map(v => v.trim().replace(/['"]/g, ''))
            .filter(Boolean);
    }
    return value;
}

// 获取文档类型
function getDocType(filename) {
    if (filename.endsWith('-design.md')) return 'design';
    if (filename.endsWith('-plan.md')) return 'plan';
    return 'unknown';
}

// 扫描文档
const documents = [];

try {
    const files = fs.readdirSync(PLANS_DIR)
        .filter(f => f.endsWith('.md'))
        .sort();

    for (const file of files) {
        const filePath = path.join(PLANS_DIR, file);
        const content = fs.readFileSync(filePath, 'utf-8');

        const frontmatter = parseFrontmatter(content);
        if (!frontmatter) continue;

        const docType = getDocType(file);

        documents.push({
            path: filePath,
            type: docType,
            ...frontmatter
        });
    }
} catch (error) {
    console.error('Error scanning plans directory:', error.message);
    console.log('[]');
    process.exit(1);
}

// 输出 JSON
console.log(JSON.stringify(documents, null, 2));
