---
title: "Facilities"
permalink: /facilities/
layout: single
author_profile: true
---

The SLAM Lab develops and tests its own aerial and ground platforms.

<style>
.fac{ --fac-line:#e3e8ee; --fac-muted:#6b7480; }
@media (prefers-color-scheme: dark){
  .fac{ --fac-line:#2b323b; --fac-muted:#8b94a0; }
}
.fac{ max-width:900px; margin:2em 0; }
.fac img, .fac video{ width:100%; display:block; border-radius:10px;
  border:1px solid var(--fac-line); }
.fac video{ background:#000; }
.fac figcaption{ font-size:.82em; color:var(--fac-muted); margin-top:.55em; }
</style>

<figure class="fac">
  <img src="slam-uav.jpg" alt="A SLAM Lab quadrotor with carbon-fiber arms and a 3D-printed body, next to its ground transmitter." loading="lazy" width="1800" height="1350">
  <figcaption>A SLAM Lab quadrotor.</figcaption>
</figure>

<figure class="fac">
  <video controls loop muted autoplay playsinline preload="metadata">
    <source src="slam-uav-demo1.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <figcaption>Quadrotor flight test inside the OU Drone Dome.</figcaption>
</figure>

<figure class="fac">
  <video controls playsinline preload="metadata">
    <source src="ground-demo.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <figcaption>Ground robot navigating an indoor environment.</figcaption>
</figure>
