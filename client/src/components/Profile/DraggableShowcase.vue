 
   <template>
    <div class="row">
  
      <div class="col-6">
        <draggable
            class="d-flex flex-row list-group"
            :component-data="{ tag: 'ul', type: 'transition-group', name: !drag ? 'flip-list' : null}"

            :list="props.list"
            handle=".drag"

            v-bind="dragOptions"
            @start="drag = true"
            @end="drag = false"
            item-key="order"
        >
          <template #item="{ element }">
            <div class="list-group-item" >
                <v-card class="d-flex flex-column align-center mr-2" rounded="0" v-if="props.type == 'stats'" style="max-width:160px">

                  <div class="d-flex flex-column align-center pb-1" v-if="!element?.type">
                    <v-card-title class="d-flex flex-row align-center justify-center" style="white-space: normal;">{{ element.data.name }}</v-card-title>
                    <v-card-text class="pt-0 pb-1">{{ element.data.count }}</v-card-text>
                  </div>

                  <div class="d-flex flex-column align-center px-2 w-100" v-else-if="element?.type == 'creating'">
                    <v-cart-title class="w-100">
                      <v-combobox class="stat_type pb-2 pt-1 ma-0"
                          v-model="statType"
                          :items="['Like', 'Dislikes', 'Workshop Count']"
                          label="Stat type"
                          density="compact"
                          hide-details
                          @update:model-value="emit('changeStatOption', statType)"
                      ></v-combobox>
                    </v-cart-title>
                    <v-card-text class="pt-0 pb-1">{{ element.data.count }}</v-card-text>
                  </div>

                  <div v-if="props.edit">
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
                            @click="emit('removeStatBlock', element.order)"
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
                  </div>
                </v-card>
            </div>
          </template>
        </draggable>
      </div>
  
      <rawDisplayer class="col-3" :value="props.list" title="List" />
    </div>
  </template>



  
  <script setup>
  import { ref, defineProps, computed, defineEmits} from 'vue';
  import draggable from 'vuedraggable'

  const props = defineProps(['list', 'type', 'edit', 'addBlock'])
  const emit = defineEmits(['changeStatOption', 'removeStatBlock'])

  let statType = ref('like') 

  const drag = ref(false);
  const dragOptions = {
    animation: 200,
    group: "description",
    disabled: false,
    ghostClass: "ghost"
  };

const canMove = (element, direction) => {
  const currentIndex = props.list.findIndex((item) => item.order === element.order);
  const new_element_pos = props.list[currentIndex + direction];
  return {'state': new_element_pos && !element.fixed, 'currentIndex': currentIndex};
};


const move =(element, direction) =>{
  const movingInfo = canMove(element, direction)
  const state = movingInfo.state
  const currentIndex = movingInfo.currentIndex

  if(state){
      const newIndex = currentIndex + direction;
      [props.list[currentIndex], props.list[newIndex]] = [props.list[newIndex], props.list[currentIndex]];
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
  