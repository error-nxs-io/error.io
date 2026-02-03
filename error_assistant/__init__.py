 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/error_assistant/__init__.py b/error_assistant/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..ede864ef52375245b9e6fd5018314d64a7dafcb1
--- /dev/null
+++ b/error_assistant/__init__.py
@@ -0,0 +1,4 @@
+"""ERROR Assistant package."""
+
+__all__ = ["__version__"]
+__version__ = "0.1.0"
 
EOF
)
