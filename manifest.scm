(use-modules (gnu packages)
	     (guix transformations))

(packages->manifest
 (list
  ;; Shell Tools
  (specification->package "bash")
  (specification->package "coreutils")
  (specification->package "git")
  (specification->package "password-store")
  (specification->package "openssh")
  ((options->transformation
    '((with-branch . "emacs-jupyter=master"))) (specification->package "emacs-jupyter"))
  (specification->package "jupyter")
  (specification->package "pandoc") 
  
  ;; Python Version
  (specification->package "python")
  (specification->package "python-pip")

  ;; Python Analysis Tools
  (specification->package "python-numpy")
  (specification->package "python-pandas")
  (specification->package "python-matplotlib")
  (specification->package "python-gast")
  (specification->package "python-levenshtein") 

  ;; Python Database Interaction
  (specification->package "python-psycopg2")
  (specification->package "python-sqlalchemy")
  (specification->package "python-sshtunnel")))
