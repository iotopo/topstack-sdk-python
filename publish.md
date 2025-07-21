# GitHub Actions 自动发布 PyPI 指南

要实现 GitHub Actions 自动发布到 PyPI，除了已经配置的 `.github/workflows/publish.yml`，还需要完成以下准备工作：

---

## 1. 配置 PyPI/TestPyPI API Token 到 GitHub Secrets

**必须操作！否则 workflow 无法上传包。**

- 登录 [PyPI](https://pypi.org/manage/account/token/) 和 [TestPyPI](https://test.pypi.org/manage/account/token/) 分别生成 API Token。
- 在 GitHub 仓库页面 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`，添加：
  - `PYPI_API_TOKEN`（正式 PyPI 的 token）
  - `TEST_PYPI_API_TOKEN`（TestPyPI 的 token）

---

## 2. 确保包元数据完整

- `pyproject.toml` 中的 `name`、`version`、`description`、`authors`、`license`、`readme` 等字段要填写完整。
- `README.md`、`LICENSE` 文件要存在于仓库根目录。

---

## 3. 确保构建产物正确

- 包结构要标准，`pyproject.toml` 配置要正确（已完成）。
- 入口文件、依赖、包名等无误。

---

## 4. Tag 规范

- 只有推送 `v1.2.3` 这样的 tag 才会自动触发发布。
- `v1.2.3-rc1`、`v1.2.3-beta1`、`v1.2.3-alpha1` 这样的 tag 会自动发布到 TestPyPI。

---

## 5. 版本号管理

- 每次发布新版本前，**务必修改 `pyproject.toml` 里的 `version` 字段**，否则 PyPI 会拒绝重复版本号的上传。

---

## 6. 可选：自动化测试

- 建议在 workflow 里加上自动化测试步骤（如 `pytest`），确保包发布前通过测试。
- 可在 `publish.yml` 的 `build` 步骤前加：
  ```yaml
      - name: Install test dependencies
        run: pip install .[dev]
      - name: Run tests
        run: pytest
  ```

---

## 7. 可选：包检查

- 可以加 `twine check dist/*` 步骤，已在 workflow 中。

---

## 8. 可选：包内容检查

- 确认 `.gitignore`、`MANIFEST.in`（如有）不会遗漏需要包含的文件。

---

## 总结

**只要完成上述 1~5 步，自动发布就能顺利运行。**  
建议加上自动化测试（第6步），这样每次发布都更安全。

如需补充自动化测试或其它发布前检查，可随时补充！ 