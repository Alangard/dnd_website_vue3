import { VueRenderer, useEditor } from '@tiptap/vue-3'
import tippy from 'tippy.js'

import MentionList from './MentionList.vue'
import store from '@/store';

export default {
  items: async ({ query }) => {

    let response = await store.dispatch('auth/getUsersList')
    return response.filter((item) => item.username && item.username.toLowerCase().startsWith(query.toLowerCase())).slice(0, 5).map((item) => item.username);
  },

  render: () => {
    let component
    let popup

    return {
      onStart: props => {
        component = new VueRenderer(MentionList, {props,editor: props.editor})

        if (!props.clientRect) {return }

        popup = tippy('body', {
          getReferenceClientRect: props.clientRect,
          appendTo: () => document.body,
          content: component.element,
          showOnCreate: true,
          interactive: true,
          trigger: 'manual',
          placement: 'bottom-start',
        })
      },

      onUpdate(props) {
        component.updateProps(props)
        if (!props.clientRect) {return}
        popup[0].setProps({getReferenceClientRect: props.clientRect})
      },

      onKeyDown(props) {
        if (props.event.key === 'Escape') {
          popup[0].hide()
          return true
        }

        return component.ref?.onKeyDown(props)
      },

      onExit() {
        popup[0].destroy()
        component.destroy()
      },
      
      // render(props) {
      //   const suggestion = props.suggestion;
      //   return (
      //     <a href={`/users/${suggestion.username}`}>
      //       {suggestion.label}
      //     </a>
      //   );
      // },
    }
  },
}