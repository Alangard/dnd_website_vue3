 
   <template>
    <div class="row">
  
      <div class="col-6">
        <draggable
            class="d-flex flex-row list-group"
            :component-data="{ tag: 'ul', type: 'transition-group', name: !drag ? 'flip-list' : null}"

            :list="list"
            handle=".drag"

            v-bind="dragOptions"
            @start="drag = true"
            @end="drag = false"
            item-key="order"
        >
          <template #item="{ element }">
            <div class="list-group-item" style="max-width:160px">
                <v-card class="d-flex flex-column align-center mr-2" rounded="0">

                    <v-card-title class="d-flex flex-row align-center justify-center" style="white-space: normal;">{{ element.name.name }}</v-card-title>
                    <v-card-text class="py-0">{{ element.name.count }}</v-card-text>

                    <v-card-actions class="py-2 px-1" width="100%" variant="tonal">
                        <v-btn class="left" 
                            :disabled="!canMove(element, -1).state"
                            @click="move(element, -1)" 
                            icon="mdi-menu-left-outline" 
                            density="compact">
                        </v-btn>
                        <v-btn class="drag"  
                            icon="mdi-drag" 
                            density="compact">
                        </v-btn>
                        <v-btn class="remove_stat_block px-0"
                            @click="removeStat(element.order)"
                            variant="plain"
                            density="comfortable" 
                            icon="mdi-close">
                        </v-btn>
                        <v-btn class="right" 
                            :disabled="!canMove(element, +1).state"
                            @click="move(element, +1)" 
                            icon="mdi-menu-right-outline" 
                            density="compact">
                        </v-btn>
                    </v-card-actions>
                </v-card>


            </div>
          </template>
        </draggable>
      </div>
  
      <rawDisplayer class="col-3" :value="list" title="List" />
    </div>
  </template>





  
  <script setup>
  import { ref, reactive, defineProps, toRaw } from 'vue';
  import draggable from 'vuedraggable'

  const props = defineProps(['list'])
  
  const list = ref(
    props.list?.map((name, index) => {
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


const removeStat =(order) => {
    const idx = list.value.findIndex((item) => item.order === order);
    list.value.splice(idx, 1)
}


const canMove = (element, direction) => {
  const currentIndex = list.value.findIndex((item) => item.order === element.order);
  const new_element_pos = list.value[currentIndex + direction];
  return {'state': new_element_pos && !element.fixed, 'currentIndex': currentIndex};
};


const move =(element, direction) =>{
    const movingInfo = canMove(element, direction)
    const state = movingInfo.state
    const currentIndex = movingInfo.currentIndex

    if(state){
        const newIndex = currentIndex + direction;
        [list.value[currentIndex], list.value[newIndex]] = [list.value[newIndex], list.value[currentIndex]];
    }
}
  
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
  
  .list-group-item .drag i {
    cursor: move;
  }
  
  </style>
  