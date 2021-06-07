<template>
  <div class="flex h-full w-full">
    <div class="border h-full">
      <div class="flex justify-between">
        <div class="font-bold">Papers</div>
        <div class="flex text-sm space-x-2 mr-2">
          <p
            class="cursor-pointer"
            v-bind:class="{
              'text-gray-900': show_all,
              'text-gray-200': !show_all,
            }"
            @click="show_all = !show_all"
          >
            <font-awesome-icon :icon="['far', 'eye']" />
          </p>
          <p class="cursor-pointer" @click="get_papers">
            <font-awesome-icon :icon="['fas', 'sync-alt']" />
          </p>
          <p class="cursor-pointer" @click="add_paper">
            <font-awesome-icon :icon="['fas', 'plus']" />
          </p>
        </div>
      </div>
      <ul class="w-64">
        <li
          v-for="paper in valid_papers"
          :key="paper.id"
          @click="current_paper = paper"
          class="border-t px-2 py-1 hover:bg-gray-200 cursor-pointer text-xs"
          v-bind:class="{
            'bg-gray-200': current_paper === paper,
            'text-gray-500': paper.removed,
          }"
        >
          <span>
            <span v-if="paper.year">[{{ paper.year }}] </span>
            <span>{{ paper.title }}</span>
          </span>
        </li>
      </ul>
    </div>
    <div class="w-full px-5">
      <div class="w-full">
        <div class="flex text-2xl mt-5">
          <input
            class="border-b border-transparent focus:outline-none focus:border-gray-500 w-full"
            type="text"
            v-model="current_paper.title"
          />
        </div>
        <div class="text-sm">
          <div class="flex mt-5">
            <a :href="current_paper.url" target="_blank" class=""
              ><font-awesome-icon :icon="['far', 'file-pdf']"
            /></a>
            <input
              class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-full"
              type="text"
              v-model="current_paper.url"
            />
            <div class="border rounded border-black px-1 cursor-pointer" @click="complete_info">complete</div>
          </div>
          <div class="flex mt-5">
            <div class="flex space-x-2">
              <div class="flex">
                <label class=""
                  ><font-awesome-icon :icon="['far', 'calendar']"
                /></label>
                <input
                  class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-8"
                  type="text"
                  v-model="current_paper.year"
                />
              </div>
              <div class="flex">
                <label class=""
                  ><font-awesome-icon :icon="['fas', 'book']"
                /></label>
                <input
                  class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-16"
                  type="text"
                  v-model="current_paper.venue"
                />
              </div>
            </div>
            <div class="flex">
              <label class=""
                ><font-awesome-icon :icon="['far', 'flag']"
              /></label>
              <input
                class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-32"
                type="text"
                v-model="current_paper.abbr"
              />
            </div>
            <div class="flex">
              <label class=""
                ><font-awesome-icon :icon="['far', 'bookmark']"
              /></label>
              <input
                class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-36"
                type="text"
                v-model="current_paper.topic"
              />
            </div>
            <div class="flex">
              <label class=""
                ><font-awesome-icon :icon="['fas', 'tags']"
              /></label>
              <input
                class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-48"
                type="text"
                v-model="tags"
              />
            </div>
          </div>
          <div class="flex mt-2">
            <label class="">
              <font-awesome-icon :icon="['fas', 'user-graduate']" />
            </label>
            <input
              class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-full"
              type="text"
              v-model="authors"
            />
          </div>
          <div class="flex mt-2">
            <label class=""
              ><font-awesome-icon :icon="['far', 'building']"
            /></label>
            <input
              class="mx-2 border-b border-transparent focus:outline-none focus:border-gray-500 w-full"
              type="text"
              v-model="organizations"
            />
          </div>
        </div>
      </div>
      <div class="mt-5">
        <div id="vditor" class="w-full h-70"></div>
      </div>
      <div class="mt-2">
        <p class="text-gray-500 text-sm">{{ tip }}</p>
      </div>
      <div class="text-xl">
        <div class="flex mt-2 space-x-3" v-if="!current_paper.removed">
          <div class="cursor-pointer hover:text-gray-600" @click="save">
            <font-awesome-icon :icon="['far', 'save']" />
          </div>
          <div class="cursor-pointer hover:text-gray-600" @click="remove_paper">
            <font-awesome-icon :icon="['far', 'trash-alt']" />
          </div>
        </div>
        <div class="flex mt-2 space-x-2" v-else>
          <div class="flex">
            <div
              class="cursor-pointer hover:text-gray-600"
              @click="restore_paper"
            >
              <font-awesome-icon :icon="['fas', 'trash-restore-alt']" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Vditor from "vditor";
import _ from "lodash";

export default {
  name: "Home",
  data() {
    return {
      api: "http://" + window.location.hostname + ":2022/api/",
      papers: [],
      current_paper: {},
      loading: false,
      editing: true,
      editor: null,
      show_all: false,
      saved_paper: "",
      saving_gap: 300 * 1000,
      tip: "",
      timer: {},
    };
  },
  mounted: function () {
    this.editor = new Vditor("vditor", {
      // height: 480,
      // toolbar: [],
      toolbarConfig: {
        pin: true,
      },
      cache: {
        enable: false,
      },
      after: () => {
        this.get_papers();
        this.timer = setInterval(this.save, this.saving_gap);
      },
      upload: {
        accept: "image/*",
        url: this.api + "upload",
        format: (files, msg) => {
          const response = JSON.parse(msg);
          return JSON.stringify({
            msg: "upload successfully",
            code: "0",
            data: {
              errFiles: [],
              succMap: _.zipObject(
                _.map(files, (file) => {
                  return file.name;
                }),
                _.map(response.filenames, (name) => {
                  return this.api + "fetch/" + name;
                })
              ),
            },
          });
        },
      },
    });
  },
  methods: {
    get_papers: function () {
      this.loading = true;
      axios
        .get(this.api + "papers")
        .then((response) => {
          this.papers = response.data.papers;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    save: function () {
      if (this.current_paper.title) {
        this.current_paper.note = this.editor.getValue();
        if (JSON.stringify(this.current_paper) != this.saved_paper) {
          this.loading = true;
          axios
            .post(this.api + "paper", this.current_paper)
            .then((response) => {
              this.current_paper._id = response.data._id;
              this.saved_paper = JSON.stringify(this.current_paper);
            })
            .finally(() => {
              this.loading = false;
              this.tip = "Last saving: " + new Date();
            });
        }
      }
    },
    remove_paper: function () {
      this.loading = true;
      axios
        .get(this.api + "paper/delete/" + this.current_paper._id)
        .then(() => {
          this.current_paper.removed = true;
        })
        .finally(() => {
          this.loading = false;
        });
      return;
    },
    restore_paper: function () {
      this.loading = true;
      axios
        .get(this.api + "paper/restore/" + this.current_paper._id)
        .then(() => {
          this.current_paper.removed = false;
        })
        .finally(() => {
          this.loading = false;
        });
      return;
    },
    add_paper: function () {
      var new_paper = {
        title: "Title",
        note: "",
      };
      this.papers.push(new_paper);
      this.current_paper = new_paper;
    },
    format_date: function (timestamp) {
      return timestamp;
    },
    complete_info: function () {
      this.loading = true;
      axios
        .get(this.api + "complete_info?url=" + this.current_paper.url)
        .then((response) => {
          let paper = response.data.paper;
          this.current_paper.title = paper.title;
          this.current_paper.year = paper.year;
          this.current_paper.authors = paper.authors;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  computed: {
    valid_papers: function () {
      if (this.show_all) {
        return this.papers;
      } else {
        var res = [];
        for (const paper of this.papers) {
          if (!paper.removed) {
            res.push(paper);
          }
        }
      }
      return res;
    },
    tags: {
      get: function () {
        if (this.current_paper.tags) {
          return _.join(this.current_paper.tags, ", ");
        } else {
          return "";
        }
      },
      set: _.debounce(function (value) {
        this.current_paper.tags = _.map(_.split(value, ","), _.trim);
      }, 500),
    },
    authors: {
      get: function () {
        if (this.current_paper.authors) {
          return _.join(this.current_paper.authors, ", ");
        } else {
          return "";
        }
      },
      set: _.debounce(function (value) {
        this.current_paper.authors = _.map(_.split(value, ","), _.trim);
      }, 500),
    },
    organizations: {
      get: function () {
        if (this.current_paper.organizations) {
          return _.join(this.current_paper.organizations, ", ");
        } else {
          return "";
        }
      },
      set: _.debounce(function (value) {
        this.current_paper.organizations = _.map(_.split(value, ","), _.trim);
      }, 500),
    },
  },
  watch: {
    current_paper: function () {
      if (this.current_paper.note) {
        this.editor.setValue(this.current_paper.note);
      } else {
        this.editor.setValue("");
      }
      this.saved_paper = JSON.stringify(this.current_paper);
    },
    valid_papers: function () {
      if (this.valid_papers.length > 0) {
        this.current_paper = this.valid_papers[this.valid_papers.length - 1];
      }
    },
  },
};
</script>

<style scoped>
@import "~vditor/dist/index.css";

.h-70 {
  height: 70vh;
}
.h-90 {
  height: 90vh;
}
</style>