---
title: "Facilities"
permalink: /facilities/
layout: single
author_profile: true
---

The SLAM Lab develops and tests its own aerial and ground platforms. Rather than
flying sealed commercial airframes, we build and modify our own, which lets us
instrument and change the parts of the system our research actually targets &mdash;
state estimation, control, and resilience to faults and attacks.

<style>
.fac{ --fac-line:#e3e8ee; --fac-muted:#6b7480; --fac-accent:#2878c4; }
@media (prefers-color-scheme: dark){
  .fac{ --fac-line:#2b323b; --fac-muted:#8b94a0; --fac-accent:#5aa9ea; }
}
.fac{ margin:2.2em 0; }
.fac h2{ margin:0 0 .15em; font-size:1.22em; }
.fac .fac-sub{ font-size:.82em; color:var(--fac-muted); margin:0 0 .9em;
  text-transform:uppercase; letter-spacing:.06em; }
.fac p{ margin:0 0 1em; }
.fac figure{ margin:1.1em 0 0; }
.fac img, .fac video{ width:100%; display:block; border-radius:10px;
  border:1px solid var(--fac-line); background:#000; }
.fac img{ background:transparent; }
.fac figcaption{ font-size:.8em; color:var(--fac-muted); margin-top:.55em; line-height:1.5; }
.fac-media{ max-width:900px; }
.fac-specs{ list-style:none; padding:0; margin:.2em 0 0;
  display:flex; flex-wrap:wrap; gap:.4em .5em; }
.fac-specs li{ font-size:.76em; color:var(--fac-muted); border:1px solid var(--fac-line);
  border-radius:999px; padding:.2em .7em; }
</style>

<div class="fac" markdown="0">
  <h2>Lab-customized UAV platforms</h2>
  <p class="fac-sub">In-house design, build, and modification</p>

  <p>Our quadrotors are assembled in the lab from carbon-fiber airframes and
  3D-printed structural parts, around an open flight-control stack. Because we
  own the full build, we can open and modify nearly every subsystem &mdash; airframe
  geometry, propulsion, flight-control firmware, state estimation, onboard
  compute, and the sensing payload &mdash; and we can add the instrumentation an
  experiment needs instead of working around a closed vendor platform.</p>

  <ul class="fac-specs">
    <li>Carbon-fiber airframe</li>
    <li>3D-printed structures</li>
    <li>Open flight-control firmware</li>
    <li>GNSS-aided navigation</li>
    <li>Swappable sensor and compute payload</li>
  </ul>

  <figure class="fac-media">
    <img src="slam-uav.jpg" alt="Lab-built quadrotor with carbon-fiber arms and a 3D-printed body, next to its ground transmitter." loading="lazy" width="1800" height="1350">
    <figcaption>A SLAM Lab quadrotor and its ground station. Airframe, wiring,
    firmware, and payload are all configured in the lab.</figcaption>
  </figure>
</div>

<div class="fac" markdown="0">
  <h2>UAV flight tests &mdash; OU Drone Dome</h2>
  <p class="fac-sub">Indoor netted flight facility</p>

  <p>Flight testing runs at the University of Oklahoma's Drone Dome, an enclosed
  netted facility. Flying indoors lets us repeat experiments year-round
  independent of weather, and test aggressive or deliberately degraded
  conditions &mdash; induced sensor faults, spoofed GNSS, and controller failures &mdash;
  safely inside the net.</p>
  <!-- Add specifics here if you want them public: flight-volume dimensions,
       motion-capture system, net height, available ground-station setup. -->

  <figure class="fac-media">
    <video controls loop muted autoplay playsinline preload="metadata">
      <source src="slam-uav-demo1.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <figcaption>Quadrotor flight test inside the OU Drone Dome.</figcaption>
  </figure>
</div>

<div class="fac" markdown="0">
  <h2>Ground robot navigation</h2>
  <p class="fac-sub">Wheeled platform testing</p>

  <p>Ground platforms let us study the same navigation and decision-making
  problems without the flight envelope, which is useful for longer-duration
  experiments and for algorithms that transfer between air and ground.</p>

  <figure class="fac-media">
    <video controls playsinline preload="metadata">
      <source src="ground-demo.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <figcaption>Ground robot navigating an indoor environment.</figcaption>
  </figure>
</div>
