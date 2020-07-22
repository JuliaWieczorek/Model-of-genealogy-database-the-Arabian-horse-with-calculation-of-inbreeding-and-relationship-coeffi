# Model of genealogy database the Arabian horse with calculation of inbreeding and relationship coefficient

The program, which was presented in this work, provides the most necessary algorithms for calculations performed in farms. It allows you to examine the genealogy of an
individual, calculate the inbreeding coefficients and affinity of individuals, show all relatives of the individual in a straight line, find both closest ancestors and all possible relatives,
find descendants, parents or grandparents. In addition, it creates opportunities for further development and extension with additional functions. All this is based on a database that
is extremely flexible: you can not only add new relationships and individuals, but you can modify it according to your needs. It contains only the basics to create a pedigree, without
imposing limits on anyone.

## Materials
60 thousand pure bred Arabian horses from the stud farm in Janów Podlaski

## Methods

The program can be divided into two parts. 
* The first one includes the relational database managed by SQLite. It supports SQLite and gives the possibility to use the database without having to run another system process. It enables entering, modifying and reading data from the database. 
* The second part is written in Python 2.7.14 programming language and supports calculation functions for estimating basic genetic factors.
