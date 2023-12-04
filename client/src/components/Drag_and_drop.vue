<!-- <template>
    <div>
      <v-row>
        <v-col cols="4" v-for="block in blocks" :key="block.id">
          <v-card
            class="draggable"
            @dragstart="startDrag(block)"
            @dragover="dragover"
            @drop="drop(block)"
            draggable="true"
          >
            <v-card-title>
              {{ block.title }}
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </template>
  
  <script setup>
  import { reactive, toRef, onMounted } from 'vue';
  
  const blocks = reactive([
    { id: 1, title: 'Block 1' },
    { id: 2, title: 'Block 2' },
    { id: 3, title: 'Block 3' },
  ]);
  
  let draggingItem = null;
  
  const startDrag = (item) => {
    draggingItem = item;
  };
  
  const dragover = (event) => {
    event.preventDefault();
  };
  
  const drop = (item) => {
    const draggingIndex = blocks.findIndex((block) => block === draggingItem);
    const dropIndex = blocks.findIndex((block) => block === item);

    console.log(draggingIndex, dropIndex)
  
    if (draggingIndex !== -1 && dropIndex !== -1 && draggingIndex !== dropIndex) {
      blocks.splice(draggingIndex, 1);
      blocks.splice(dropIndex, 0, draggingItem);
    }
  
    draggingItem = null;
  };
  
  const draggable = (el) => {
    const cards = el.getElementsByClassName('draggable');
  
    for (const card of cards) {
      card.addEventListener('dragstart', (event) => {
        event.dataTransfer.setData('text/plain', null);
      });
    }
  };
  
  onMounted(() => {
    draggable(document.body);
  });
  </script>
  
  <style>
  .draggable {
    cursor: move;
  }
  </style>
   -->


  
<template>
    <div class="row">
      <!-- <div class="col-2">
        <v-btn class="btn btn-secondary button" @click="sort">
          To original order
        </v-btn>
      </div> -->
  
      <div class="col-6">
        <slot name="title"></slot>
        <draggable
          class="d-flex flex-row list-group"
          :component-data="{ tag: 'ul', type: 'transition-group', name: !drag ? 'flip-list' : null}"
          v-model="list"
          v-bind="dragOptions"
          @start="drag = true"
          @end="drag = false"
          item-key="order"
        >
          <template #item="{ element }">
            <div class="list-group-item">
              <!-- <slot name="list_item"></slot> -->
              <!-- <v-icon
                :class="{ 'fa fa-anchor': element.fixed, 'glyphicon glyphicon-pushpin': !element.fixed }"
                @click="element.fixed = !element.fixed"
                aria-hidden="true"
              ></v-icon>
              {{ element.name }} -->
            </div>
          </template>
        </draggable>
      </div>
  
      <rawDisplayer class="col-3" :value="list" title="List" />
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, defineProps } from 'vue';
  import draggable from 'vuedraggable'

  const props = defineProps(['test_list'])
  
  const message = [
    "vue.draggable",
    "draggable",
    "component",
    "for",
    "vue.js 2.0",
    "based",
    "on",
    "Sortablejs"
  ];
  
  const list = ref(
    props.test_list?.map((name, index) => {
      return { name, order: index + 1 };
    })
  );
  
  const drag = ref(false);
  
  const dragOptions = {
    animation: 200,
    group: "description",
    disabled: false,
    ghostClass: "ghost"
  };
  
  const sort = () => {
    list.value = list.value.sort((a, b) => a.order - b.order);
  };
  </script>
  
  <style>
  .button {
    margin-top: 35px;
  }
  
  .flip-list-move {
    transition: transform 0.5s;
  }
  
  .no-move {
    transition: transform 0s;
  }
  
  .ghost {
    opacity: 0.5;
    background: #c8ebfb;
  }
  
  .list-group {
    min-height: 20px;
  }
  
  .list-group-item {
    cursor: move;
  }
  
  .list-group-item i {
    cursor: pointer;
  }
  </style>
  