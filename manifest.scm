(use-modules (gnu packages)
	     (guix transformations))

(packages->manifest
 (list
  ;; Shell Tools
  (specification->package "bash")
  (specification->package "coreutils")
  (specification->package "git")
  (specification->package "password-store")

  ;; Framework
  ;; ((options->transformation
  ;;   '((with-latest . "tensorflow")
  ;;     (with-latest . "glibc")))
  ;;  (specification->package "tensorflow"))
  ;; (specification->package "tensorflow")
  
  ;; Python Version
  (specification->package "python")

  ;; Python Analysis Tools
  ;; ((options->transformation
  ;;   '((with-input . "python-pyparsing=python-pyparsing@3.0.6")
  ;;     (without-tests . "python-pydot")
  ;;     (without-tests . "python-keras")))
  ;;  (specification->package "python-keras"))
  (specification->package "python-numpy")
  (specification->package "python-gast")
  (specification->package "python-matplotlib")
  (specification->package "python-pandas")
  (specification->package "python-plotly")

  ;; Python Database Interaction
  (specification->package "python-psycopg2")
  (specification->package "python-sqlalchemy")
  (specification->package "python-sshtunnel")))
