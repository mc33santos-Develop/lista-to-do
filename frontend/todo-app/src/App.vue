<script setup>

</script>

<template>
  <main>
    <router-view/>
  </main>
</template>

<style>

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: #f0f2f5;
  margin: 0;
  display: flex;
  justify-content: center;
  padding-top: 40px;
  /* Seus estilos de fundo */
  background-color: #19a3c9; 
}
main {
  width: 100%;

}
/* Estilos globais dos seus arquivos */
:root {
 --primary-color: #3498db;
 --card-bg: rgba(255, 255, 255, 0.9);
 --text-color: #34495e;
 --placeholder-color: #95a5a6;
 --danger-color: #e74c3c;
--light-gray: #ecf0f1;
}
</style>