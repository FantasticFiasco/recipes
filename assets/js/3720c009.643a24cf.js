"use strict";(self.webpackChunkrecept=self.webpackChunkrecept||[]).push([[3751],{9861:(t,e,a)=>{a.r(e),a.d(e,{default:()=>p});a(7294);var s=a(512),r=a(1944),l=a(5281),n=a(5999);const c=()=>(0,n.I)({id:"theme.tags.tagsPageTitle",message:"Tags",description:"The title of the tag list page"});var i=a(3008),g=a(2503);const o={tag:"tag_Nnez"};var u=a(5893);function h(t){let{letterEntry:e}=t;return(0,u.jsxs)("article",{children:[(0,u.jsx)(g.Z,{as:"h2",id:e.letter,children:e.letter}),(0,u.jsx)("ul",{className:"padding--none",children:e.tags.map((t=>(0,u.jsx)("li",{className:o.tag,children:(0,u.jsx)(i.Z,{...t})},t.permalink)))}),(0,u.jsx)("hr",{})]})}function d(t){let{tags:e}=t;const a=function(t){const e={};return Object.values(t).forEach((t=>{const a=function(t){return t[0].toUpperCase()}(t.label);e[a]??=[],e[a].push(t)})),Object.entries(e).sort(((t,e)=>{let[a]=t,[s]=e;return a.localeCompare(s)})).map((t=>{let[e,a]=t;return{letter:e,tags:a.sort(((t,e)=>t.label.localeCompare(e.label)))}}))}(e);return(0,u.jsx)("section",{className:"margin-vert--lg",children:a.map((t=>(0,u.jsx)(h,{letterEntry:t},t.letter)))})}var j=a(197);function m(t){let{title:e}=t;return(0,u.jsxs)(u.Fragment,{children:[(0,u.jsx)(r.d,{title:e}),(0,u.jsx)(j.Z,{tag:"doc_tags_list"})]})}function x(t){let{tags:e,title:a}=t;return(0,u.jsx)(r.FG,{className:(0,s.Z)(l.k.page.docsTagsListPage),children:(0,u.jsx)("div",{className:"container margin-vert--lg",children:(0,u.jsx)("div",{className:"row",children:(0,u.jsxs)("main",{className:"col col--8 col--offset-2",children:[(0,u.jsx)(g.Z,{as:"h1",children:a}),(0,u.jsx)(d,{tags:e})]})})})})}function p(t){const e=c();return(0,u.jsxs)(u.Fragment,{children:[(0,u.jsx)(m,{...t,title:e}),(0,u.jsx)(x,{...t,title:e})]})}},3008:(t,e,a)=>{a.d(e,{Z:()=>c});a(7294);var s=a(512),r=a(9960);const l={tag:"tag_zVej",tagRegular:"tagRegular_sFm0",tagWithCount:"tagWithCount_h2kH"};var n=a(5893);function c(t){let{permalink:e,label:a,count:c}=t;return(0,n.jsxs)(r.Z,{href:e,className:(0,s.Z)(l.tag,c?l.tagWithCount:l.tagRegular),children:[a,c&&(0,n.jsx)("span",{children:c})]})}}}]);