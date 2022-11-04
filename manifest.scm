(use-modules (gnu packages)
	     (guix transformations))

(packages->manifest
 (list
  ;; Shell Tools
  (specification->package "bash")
  (specification->package "coreutils")
  (specification->package "password-store")
  (specification->package "git")
  
  ;; Python Version
  (specification->package "python")

  ;; Analysis Tools
  (specification->package "python-numpy")
  (specification->package "python-pandas")
  (specification->package "python-matplotlib")
  (specification->package "tensorflow")
  ((options->transformation
    '((with-input . "python-pyparsing=python-pyparsing@3.0.6")
      (without-tests . "python-pydot")
      (without-tests . "python-keras")))
   (specification->package "python-keras"))


  ;; Database Interaction
  (specification->package "python-psycopg2")
  (specification->package "python-sqlalchemy")
  (specification->package "python-sshtunnel")))
