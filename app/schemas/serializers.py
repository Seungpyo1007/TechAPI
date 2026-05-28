"""Builders that turn ORM models into response schemas (URLs, embeds, §7.4 refs)."""

from __future__ import annotations

from app.config import settings
from app.models.brand import Brand
from app.models.cpu import CPU
from app.models.gpu import DiscreteGPU
from app.models.smartphone import Smartphone
from app.models.soc import SoC
from app.schemas.brand import BrandRead, BrandSummary
from app.schemas.common import ManufacturerRef, ResourceRef
from app.schemas.cpu import CPURead
from app.schemas.gpu import GPURead
from app.schemas.smartphone import ScoreRead, SmartphoneRead
from app.schemas.soc import SoCManufacturer, SoCRead, SoCSummary
from app.services.scoring import Scores

PREFIX = settings.api_version_prefix


def url_for(resource: str, slug: str) -> str:
    """Build a versioned resource URL, e.g. ``/v1/smartphones/galaxy-s25``."""
    return f"{PREFIX}/{resource}/{slug}"


def resource_ref(resource: str, slug: str, name: str) -> ResourceRef:
    return ResourceRef(slug=slug, name=name, url=url_for(resource, slug))


def brand_summary(brand: Brand) -> BrandSummary:
    assert brand.id is not None
    return BrandSummary(
        id=brand.id,
        slug=brand.slug,
        name=brand.name,
        country=brand.country,
        url=url_for("brands", brand.slug),
    )


def brand_read(brand: Brand) -> BrandRead:
    assert brand.id is not None
    return BrandRead(
        id=brand.id,
        slug=brand.slug,
        name=brand.name,
        country=brand.country,
        founded_year=brand.founded_year,
        logo_url=brand.logo_url,
        website=brand.website,
        description_en=brand.description_en,
        description_ko=brand.description_ko,
        url=url_for("brands", brand.slug),
    )


def _manufacturer_ref(manufacturer: Brand) -> SoCManufacturer:
    return SoCManufacturer(
        slug=manufacturer.slug,
        name=manufacturer.name,
        url=url_for("brands", manufacturer.slug),
    )


def soc_summary(soc: SoC, manufacturer: Brand) -> SoCSummary:
    assert soc.id is not None
    return SoCSummary(
        id=soc.id,
        slug=soc.slug,
        name=soc.name,
        manufacturer=_manufacturer_ref(manufacturer),
        process_nm=soc.process_nm,
        gpu_name=soc.gpu_name,
        url=url_for("socs", soc.slug),
    )


def soc_read(soc: SoC, manufacturer: Brand) -> SoCRead:
    assert soc.id is not None
    return SoCRead(
        id=soc.id,
        slug=soc.slug,
        name=soc.name,
        manufacturer=_manufacturer_ref(manufacturer),
        release_date=soc.release_date,
        process_nm=soc.process_nm,
        transistors_billion=soc.transistors_billion,
        cpu_config=soc.cpu_config,
        gpu_name=soc.gpu_name,
        gpu_cores=soc.gpu_cores,
        gpu_clock_mhz=soc.gpu_clock_mhz,
        npu_tops=soc.npu_tops,
        modem=soc.modem,
        verified=soc.verified,
        source_urls=soc.source_urls,
        created_at=soc.created_at,
        updated_at=soc.updated_at,
        url=url_for("socs", soc.slug),
    )


def gpu_read(gpu: DiscreteGPU, manufacturer: Brand) -> GPURead:
    assert gpu.id is not None
    return GPURead(
        id=gpu.id,
        slug=gpu.slug,
        name=gpu.name,
        manufacturer=ManufacturerRef(
            slug=manufacturer.slug,
            name=manufacturer.name,
            url=url_for("brands", manufacturer.slug),
        ),
        architecture=gpu.architecture,
        release_date=gpu.release_date,
        msrp_usd=gpu.msrp_usd,
        cuda_cores=gpu.cuda_cores,
        stream_processors=gpu.stream_processors,
        rt_cores=gpu.rt_cores,
        tensor_cores=gpu.tensor_cores,
        memory_gb=gpu.memory_gb,
        memory_type=gpu.memory_type,
        memory_bus_bit=gpu.memory_bus_bit,
        memory_bandwidth_gbps=gpu.memory_bandwidth_gbps,
        base_clock_mhz=gpu.base_clock_mhz,
        boost_clock_mhz=gpu.boost_clock_mhz,
        tdp_w=gpu.tdp_w,
        pcie_version=gpu.pcie_version,
        blender_score=gpu.blender_score,
        verified=gpu.verified,
        source_urls=gpu.source_urls,
        url=url_for("gpus", gpu.slug),
    )


def cpu_read(cpu: CPU, manufacturer: Brand) -> CPURead:
    assert cpu.id is not None
    return CPURead(
        id=cpu.id,
        slug=cpu.slug,
        name=cpu.name,
        manufacturer=ManufacturerRef(
            slug=manufacturer.slug,
            name=manufacturer.name,
            url=url_for("brands", manufacturer.slug),
        ),
        release_date=cpu.release_date,
        segment=cpu.segment,
        architecture=cpu.architecture,
        socket=cpu.socket,
        process_node=cpu.process_node,
        cores=cpu.cores,
        threads=cpu.threads,
        p_cores=cpu.p_cores,
        e_cores=cpu.e_cores,
        base_clock_ghz=cpu.base_clock_ghz,
        boost_clock_ghz=cpu.boost_clock_ghz,
        l3_cache_mb=cpu.l3_cache_mb,
        tdp_w=cpu.tdp_w,
        max_tdp_w=cpu.max_tdp_w,
        integrated_graphics=cpu.integrated_graphics,
        memory_support=cpu.memory_support,
        msrp_usd=cpu.msrp_usd,
        verified=cpu.verified,
        source_urls=cpu.source_urls,
        created_at=cpu.created_at,
        updated_at=cpu.updated_at,
        url=url_for("cpus", cpu.slug),
    )


def smartphone_read(
    phone: Smartphone,
    brand: Brand,
    soc: SoC,
    soc_manufacturer: Brand,
    scores: Scores,
) -> SmartphoneRead:
    assert phone.id is not None
    return SmartphoneRead(
        id=phone.id,
        slug=phone.slug,
        name=phone.name,
        brand=brand_summary(brand),
        soc=soc_summary(soc, soc_manufacturer),
        release_date=phone.release_date,
        msrp_usd=phone.msrp_usd,
        ram_gb=phone.ram_gb,
        storage_options_gb=phone.storage_options_gb,
        display=phone.display,
        cameras=phone.cameras,
        battery_mah=phone.battery_mah,
        charging_wired_w=phone.charging_wired_w,
        charging_wireless_w=phone.charging_wireless_w,
        weight_g=phone.weight_g,
        dimensions=phone.dimensions,
        ip_rating=phone.ip_rating,
        os=phone.os,
        os_version=phone.os_version,
        connectivity=phone.connectivity,
        image_url=phone.image_url,
        images=phone.images,
        score=ScoreRead(
            algorithm_version=scores.algorithm_version,
            overall=scores.overall,
            performance=scores.performance,
            camera=scores.camera,
            battery=scores.battery,
            display=scores.display,
            value=scores.value,
        ),
        verified=phone.verified,
        source_urls=phone.source_urls,
        created_at=phone.created_at,
        updated_at=phone.updated_at,
    )
